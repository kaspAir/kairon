from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import Any

from app.domains.decision.models import Decision, DecisionVariant
from app.shared.i18n import translate


SEVERITY_RANK = {"low": 1, "medium": 2, "high": 3, "critical": 4}
CONFIDENCE_RANK = {"low": 1, "medium": 2, "high": 3}


def _as_float(value: Any, default: float = 0.0) -> float:
    if value in (None, ""):
        return default
    if isinstance(value, Decimal):
        return float(value)
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _as_int(value: Any, default: int = 0) -> int:
    if value in (None, ""):
        return default
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return default


def _latest_simulation_for_variant(variant: DecisionVariant):
    runs = []
    for scenario in getattr(variant, "scenarios", []) or []:
        runs.extend(getattr(scenario, "simulation_runs", []) or [])
    if not runs:
        return None
    return sorted(runs, key=lambda run: getattr(run, "created_at", None), reverse=True)[0]


def _variant_net_effect(variant: DecisionVariant) -> float:
    latest_run = _latest_simulation_for_variant(variant)
    if latest_run is not None and getattr(latest_run, "impact_assessment", None) is not None:
        return _as_float(latest_run.impact_assessment.net_impact)
    return _as_float(getattr(variant, "expected_benefit", 0)) - _as_float(getattr(variant, "estimated_cost", 0))


def _dominant_risk_name(decision: Decision) -> str | None:
    risks = list(getattr(decision, "risk_assessments", []) or [])
    risk_contexts = [obj for obj in getattr(decision, "context_objects", []) or [] if getattr(obj, "context_type", "") == "risk"]

    if risks:
        risk = sorted(risks, key=lambda item: SEVERITY_RANK.get((item.severity or "").lower(), 0), reverse=True)[0]
        return getattr(risk, "summary", None)

    if risk_contexts:
        return getattr(risk_contexts[0], "name", None)

    return None


def _has_governance_review(decision: Decision) -> bool:
    return bool(getattr(decision, "approval_records", []) or [])


def _has_observations(decision: Decision) -> bool:
    return bool(getattr(decision, "observation_records", []) or [])


def _has_simulations(decision: Decision) -> bool:
    return any(getattr(scenario, "simulation_runs", []) for scenario in getattr(decision, "scenarios", []) or [])


def _scenario_count(decision: Decision) -> int:
    return len(getattr(decision, "scenarios", []) or [])


def _variant_count(decision: Decision) -> int:
    return len(getattr(decision, "variants", []) or [])


def _risk_count(decision: Decision) -> int:
    context_risks = [obj for obj in getattr(decision, "context_objects", []) or [] if getattr(obj, "context_type", "") == "risk"]
    return len(getattr(decision, "risk_assessments", []) or []) + len(context_risks)


def _simulation_count(decision: Decision) -> int:
    return sum(len(getattr(scenario, "simulation_runs", []) or []) for scenario in getattr(decision, "scenarios", []) or [])


def build_decision_readiness(decision: Decision, language: str = "de") -> dict:
    variants = _variant_count(decision)
    scenarios = _scenario_count(decision)
    simulations = _simulation_count(decision)
    risks = _risk_count(decision)
    governance_ready = _has_governance_review(decision)
    observations = _has_observations(decision)

    reasons: list[str] = []
    missing: list[str] = []
    state = "draft"

    if variants:
        state = "options_prepared"
        reasons.append(translate("decision_insight.reason.variants_exist", language=language))
    else:
        missing.append(translate("decision_insight.missing.variants", language=language))

    if scenarios:
        state = "scenario_ready"
        reasons.append(translate("decision_insight.reason.scenarios_exist", language=language))
    else:
        missing.append(translate("decision_insight.missing.scenarios", language=language))

    if simulations:
        state = "simulation_ready"
        reasons.append(translate("decision_insight.reason.simulations_exist", language=language))
    else:
        missing.append(translate("decision_insight.missing.simulations", language=language))

    if risks:
        state = "risk_reviewed" if simulations else state
        reasons.append(translate("decision_insight.reason.risks_exist", language=language))
    else:
        missing.append(translate("decision_insight.missing.risks", language=language))

    if governance_ready:
        state = "governance_ready"
        reasons.append(translate("decision_insight.reason.governance_exists", language=language))
    else:
        missing.append(translate("decision_insight.governance_pending", language=language))

    if simulations and not observations:
        missing.append(translate("decision_insight.missing_observations", language=language))

    if observations:
        state = "reassessment_needed"
        reasons.append(translate("decision_insight.reason.observations_exist", language=language))

    return {
        "state": state,
        "label": translate(f"decision_insight.readiness.state.{state}", language=language),
        "reasons": reasons,
        "missing": missing,
    }


def identify_strongest_option(decision: Decision, language: str = "de") -> dict | None:
    variants = list(getattr(decision, "variants", []) or [])
    if len(variants) < 2:
        return None

    ranked = sorted(variants, key=_variant_net_effect, reverse=True)
    strongest = ranked[0]
    second = ranked[1]
    strongest_effect = _variant_net_effect(strongest)
    second_effect = _variant_net_effect(second)

    if strongest_effect == second_effect:
        return None

    return {
        "variant_id": strongest.id,
        "variant_name": strongest.name,
        "net_effect": strongest_effect,
        "reason": translate(
            "decision_insight.strongest_option.reason",
            language=language,
            option=strongest.name,
        ),
    }


def build_key_findings(decision: Decision, language: str = "de") -> list[str]:
    findings: list[str] = []
    variants = _variant_count(decision)
    scenarios = _scenario_count(decision)
    simulations = _simulation_count(decision)
    risks = _risk_count(decision)

    if variants:
        findings.append(translate("decision_insight.finding.variants", language=language, count=variants))
    if scenarios:
        findings.append(translate("decision_insight.finding.scenarios", language=language, count=scenarios))
    if simulations:
        findings.append(translate("decision_insight.finding.simulations", language=language, count=simulations))

    strongest = identify_strongest_option(decision, language=language)
    if strongest:
        findings.append(translate("decision_insight.finding.strongest_option", language=language, option=strongest["variant_name"]))
    else:
        findings.append(translate("decision_insight.not_enough_data", language=language))

    dominant_risk = _dominant_risk_name(decision)
    if dominant_risk:
        findings.append(translate("decision_insight.finding.central_risk", language=language, risk=dominant_risk))
    elif risks == 0:
        findings.append(translate("decision_insight.finding.no_risks", language=language))

    if not _has_observations(decision):
        findings.append(translate("decision_insight.missing_observations", language=language))

    return findings


def determine_next_recommended_step(decision: Decision, language: str = "de") -> dict:
    if _variant_count(decision) == 0:
        key = "define_options"
    elif _scenario_count(decision) == 0:
        key = "create_scenarios"
    elif _simulation_count(decision) == 0:
        key = "run_simulations"
    elif _risk_count(decision) == 0:
        key = "validate_risks"
    elif not _has_governance_review(decision):
        key = "prepare_governance"
    elif not _has_observations(decision):
        key = "capture_observations"
    else:
        key = "review_reassessment"

    return {
        "key": key,
        "label": translate(f"decision_insight.next_step.{key}.label", language=language),
        "reason": translate(f"decision_insight.next_step.{key}.reason", language=language),
    }


def _base_lever_values(decision: Decision) -> dict[str, Any]:
    first_variant = (getattr(decision, "variants", []) or [None])[0]
    first_scenario = (getattr(decision, "scenarios", []) or [None])[0]
    dominant_risk = _dominant_risk_name(decision)

    return {
        "estimated_cost": _as_float(getattr(first_variant, "estimated_cost", 0)),
        "expected_benefit": _as_float(getattr(first_variant, "expected_benefit", 0)),
        "case_volume": _as_int(getattr(first_scenario, "case_volume", 0)),
        "processing_minutes_per_case": _as_float(getattr(first_scenario, "processing_minutes_per_case", 0)),
        "hourly_cost": _as_float(getattr(first_scenario, "hourly_cost", 0)),
        "risk_severity": "medium" if dominant_risk else "low",
        "confidence": "medium",
        "time_horizon_years": 1,
    }


def _adjusted_values(decision: Decision, adjusted_values: dict[str, Any] | None) -> dict[str, Any]:
    values = _base_lever_values(decision)
    if not adjusted_values:
        return values

    for key in values:
        if key not in adjusted_values or adjusted_values[key] in (None, ""):
            continue
        if key in {"risk_severity", "confidence"}:
            values[key] = str(adjusted_values[key])
        elif key in {"case_volume", "time_horizon_years"}:
            values[key] = _as_int(adjusted_values[key], values[key])
        else:
            values[key] = _as_float(adjusted_values[key], values[key])
    return values


def build_decision_levers(decision: Decision, adjusted_values: dict[str, Any] | None = None, language: str = "de") -> list[dict]:
    values = _adjusted_values(decision, adjusted_values)
    return [
        {"key": "estimated_cost", "label": translate("decision_insight.lever.estimated_cost", language=language), "value": values["estimated_cost"], "type": "number"},
        {"key": "expected_benefit", "label": translate("decision_insight.lever.expected_benefit", language=language), "value": values["expected_benefit"], "type": "number"},
        {"key": "case_volume", "label": translate("decision_insight.lever.case_volume", language=language), "value": values["case_volume"], "type": "number"},
        {"key": "processing_minutes_per_case", "label": translate("decision_insight.lever.processing_minutes_per_case", language=language), "value": values["processing_minutes_per_case"], "type": "number"},
        {"key": "hourly_cost", "label": translate("decision_insight.lever.hourly_cost", language=language), "value": values["hourly_cost"], "type": "number"},
        {"key": "time_horizon_years", "label": translate("decision_insight.time_horizon", language=language), "value": values["time_horizon_years"], "type": "number"},
        {"key": "risk_severity", "label": translate("decision_insight.lever.risk_severity", language=language), "value": values["risk_severity"], "type": "select", "options": ["low", "medium", "high", "critical"]},
        {"key": "confidence", "label": translate("decision_insight.lever.confidence", language=language), "value": values["confidence"], "type": "select", "options": ["low", "medium", "high"]},
    ]


def preview_decision_consequences(decision: Decision, adjusted_values: dict[str, Any] | None = None, language: str = "de") -> dict:
    base = _base_lever_values(decision)
    current = _adjusted_values(decision, adjusted_values)

    annual_processing_cost = (
        _as_float(current["case_volume"])
        * _as_float(current["processing_minutes_per_case"])
        / 60.0
        * _as_float(current["hourly_cost"])
    )
    horizon = max(_as_int(current["time_horizon_years"], 1), 1)
    cumulative_cost = annual_processing_cost * horizon
    cumulative_benefit = _as_float(current["expected_benefit"]) * horizon
    net_effect = cumulative_benefit - cumulative_cost - _as_float(current["estimated_cost"])

    base_annual_processing_cost = (
        _as_float(base["case_volume"])
        * _as_float(base["processing_minutes_per_case"])
        / 60.0
        * _as_float(base["hourly_cost"])
    )
    base_net_effect = (_as_float(base["expected_benefit"]) * max(_as_int(base["time_horizon_years"], 1), 1)) - base_annual_processing_cost - _as_float(base["estimated_cost"])

    messages = []
    if current["case_volume"] and current["processing_minutes_per_case"] and current["hourly_cost"]:
        messages.append(
            translate(
                "decision_insight.consequence.cost_over_time",
                language=language,
                cost=round(cumulative_cost, 2),
                years=horizon,
            )
        )
        messages.append(
            translate(
                "decision_insight.consequence.net_effect",
                language=language,
                net=round(net_effect, 2),
            )
        )
    else:
        messages.append(translate("decision_insight.consequence.missing_time_data", language=language))

    if SEVERITY_RANK.get(str(current["risk_severity"]).lower(), 0) >= 3:
        messages.append(translate("decision_insight.consequence.risk_review", language=language))

    if CONFIDENCE_RANK.get(str(current["confidence"]).lower(), 0) <= 1:
        messages.append(translate("decision_insight.consequence.low_confidence", language=language))

    return {
        "annual_processing_cost": annual_processing_cost,
        "cumulative_cost": cumulative_cost,
        "cumulative_benefit": cumulative_benefit,
        "net_effect": net_effect,
        "base_net_effect": base_net_effect,
        "delta_net_effect": net_effect - base_net_effect,
        "messages": messages,
    }


def build_decision_insight_summary(decision: Decision, adjusted_values: dict[str, Any] | None = None, language: str = "de") -> dict:
    readiness = build_decision_readiness(decision, language=language)
    strongest = identify_strongest_option(decision, language=language)
    variants = _variant_count(decision)
    scenarios = _scenario_count(decision)
    risks = _risk_count(decision)
    simulations = _simulation_count(decision)

    summary_key = "decision_insight.summary.with_data" if variants or scenarios or risks or simulations else "decision_insight.summary.empty"
    summary = translate(
        summary_key,
        language=language,
        variants=variants,
        scenarios=scenarios,
        risks=risks,
        simulations=simulations,
        readiness=readiness["label"],
    )

    if strongest:
        summary = f"{summary} {translate('decision_insight.summary.strongest_option', language=language, option=strongest['variant_name'])}"
    else:
        summary = f"{summary} {translate('decision_insight.not_enough_data', language=language)}"

    return {
        "summary": summary,
        "readiness": readiness,
        "key_findings": build_key_findings(decision, language=language),
        "next_step": determine_next_recommended_step(decision, language=language),
        "strongest_option": strongest,
        "levers": build_decision_levers(decision, adjusted_values=adjusted_values, language=language),
        "consequence_preview": preview_decision_consequences(decision, adjusted_values=adjusted_values, language=language),
    }
