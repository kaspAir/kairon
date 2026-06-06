from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import Any

from app.domains.context.types import CONTEXT_TYPE_LABELS
from app.shared.i18n import t


@dataclass(frozen=True)
class NarrativeItem:
    id: str | None
    title: str
    description: str | None
    item_type: str
    confidence: str | None = None
    owner: str | None = None


def _as_number(value: Any) -> float:
    if value is None:
        return 0.0
    if isinstance(value, Decimal):
        return float(value)
    return float(value)


def _context_item(obj) -> dict:
    return {
        "id": getattr(obj, "id", None),
        "title": getattr(obj, "name", None),
        "description": getattr(obj, "description", None),
        "type": getattr(obj, "context_type", None),
        "type_label": t(f"decision_narrative.context.type.{getattr(obj, 'context_type', '')}")
        if getattr(obj, "context_type", None)
        else CONTEXT_TYPE_LABELS.get(getattr(obj, "context_type", ""), getattr(obj, "context_type", "")),
        "confidence": getattr(obj, "confidence", None),
        "owner": getattr(obj, "owner", None),
        "source": getattr(obj, "source", None),
        "metadata": getattr(obj, "metadata_json", None) or {},
    }


def _scenario_item(scenario) -> dict:
    latest_run = None
    if getattr(scenario, "simulation_runs", None):
        latest_run = sorted(scenario.simulation_runs, key=lambda run: run.created_at, reverse=True)[0]
    impact = latest_run.impact_assessment if latest_run and latest_run.impact_assessment else None
    return {
        "id": scenario.id,
        "title": scenario.name,
        "description": scenario.description,
        "type": "scenario",
        "case_volume": scenario.case_volume,
        "processing_minutes_per_case": _as_number(scenario.processing_minutes_per_case),
        "hourly_cost": _as_number(scenario.hourly_cost),
        "status": scenario.status,
        "impact": {
            "net_impact": _as_number(impact.net_impact),
            "benefit_impact": _as_number(impact.benefit_impact),
            "cost_impact": _as_number(impact.cost_impact),
            "confidence_score": _as_number(impact.confidence_score),
        } if impact else None,
    }


def _variant_item(variant) -> dict:
    return {
        "id": variant.id,
        "title": variant.name,
        "description": variant.description,
        "type": "variant",
        "estimated_cost": _as_number(variant.estimated_cost),
        "expected_benefit": _as_number(variant.expected_benefit),
        "status": variant.status,
        "scenarios": [_scenario_item(scenario) for scenario in getattr(variant, "scenarios", [])],
    }


def _risk_assessment_item(risk) -> dict:
    return {
        "id": risk.id,
        "title": risk.summary,
        "description": risk.mitigation,
        "type": "risk",
        "severity": risk.severity,
        "status": risk.status,
    }


def _observation_item(record) -> dict:
    return {
        "id": record.id,
        "title": record.comment or t("decision_narrative.reassessment.observations"),
        "description": record.actual_risks or record.expected_risks,
        "type": "observation",
        "observed_at": record.observed_at,
        "expected_benefit": _as_number(record.expected_benefit),
        "actual_benefit": _as_number(record.actual_benefit),
        "expected_cost": _as_number(record.expected_cost),
        "actual_cost": _as_number(record.actual_cost),
    }


def _first(items: list[dict], count: int = 3) -> list[dict]:
    return [item for item in items if item.get("title")][:count]


def build_decision_narrative(decision) -> dict:
    context_items = [_context_item(obj) for obj in getattr(decision, "context_objects", [])]
    by_type: dict[str, list[dict]] = {}
    for item in context_items:
        by_type.setdefault(item.get("type") or "unknown", []).append(item)

    risk_items = by_type.get("risk", []) + [_risk_assessment_item(risk) for risk in getattr(decision, "risk_assessments", [])]
    process_items = by_type.get("process", [])
    constraint_items = by_type.get("constraint", [])
    organization_items = by_type.get("organization", [])
    workforce_items = by_type.get("workforce", [])
    assumption_items = by_type.get("assumption", [])
    metric_items = by_type.get("metric", [])
    cost_items = by_type.get("cost", [])
    external_items = by_type.get("external_factor", [])

    variants = [_variant_item(variant) for variant in getattr(decision, "variants", [])]
    scenarios = [_scenario_item(scenario) for scenario in getattr(decision, "scenarios", [])]
    observations = [_observation_item(record) for record in sorted(getattr(decision, "observation_records", []), key=lambda item: item.observed_at, reverse=True)]

    why_text = decision.context or None
    option_count = len(variants) or len(scenarios)
    central_risks = _first(risk_items, 3)
    future_items = _first(assumption_items + metric_items + scenarios, 4)

    brief_parts = []
    if why_text:
        brief_parts.append(t("decision_narrative.brief.because", title=decision.title, reason=why_text))
    else:
        brief_parts.append(t("decision_narrative.brief.empty"))
    brief_parts.append(t("decision_narrative.brief.options", count=option_count) if option_count else t("decision_narrative.brief.no_options"))
    brief_parts.append(t("decision_narrative.brief.risks", items=", ".join(item["title"] for item in central_risks)) if central_risks else t("decision_narrative.brief.no_risks"))
    brief_parts.append(t("decision_narrative.brief.future", items=", ".join(item["title"] for item in future_items[:3])) if future_items else t("decision_narrative.brief.no_future"))
    brief_parts.append(t("decision_narrative.brief.reassessment") if observations or decision.status in {"observed", "reassessment_needed", "reassessing"} else t("decision_narrative.brief.no_reassessment"))

    review_points = _first(assumption_items + metric_items + risk_items + observations, 5)

    return {
        "brief": brief_parts,
        "why": {
            "description": why_text,
            "owner": getattr(decision, "created_by", None),
            "status": getattr(decision, "status", None),
        },
        "first_screen": {
            "option_count": option_count,
            "risk_count": len(risk_items),
            "review_status": getattr(decision, "status", None),
            "central_risks": central_risks[:2],
        },
        "circumstances": {
            "processes": process_items,
            "risks": risk_items,
            "constraints": constraint_items,
            "roles": organization_items + workforce_items,
            "external_factors": external_items,
            "key_context": _first(process_items + constraint_items + organization_items + workforce_items + external_items, 6),
        },
        "options": {
            "variants": variants,
            "scenarios": scenarios,
        },
        "expected_future": {
            "assumptions": assumption_items,
            "metrics": metric_items + cost_items,
            "scenarios": scenarios,
            "has_simulations": any(item.get("impact") for item in scenarios),
        },
        "reassessment": {
            "status": getattr(decision, "status", None),
            "observations": observations,
            "review_points": review_points,
        },
    }


def build_relationship_awareness(decision) -> dict:
    """Backward-compatible, lightweight awareness view from existing context data.

    V0.x keeps relationships lightweight. This function intentionally exposes
    decision-oriented names and a summary_counts key for existing regression
    contracts.
    """
    context_items = [_context_item(obj) for obj in getattr(decision, "context_objects", [])]
    buckets = {
        "processes": [],
        "risks": [],
        "policies": [],
        "scenarios": [],
        "observations": [],
        "governance_objects": [],
    }
    for item in context_items:
        item_type = item.get("type")
        if item_type == "process":
            buckets["processes"].append(item)
        elif item_type == "risk":
            buckets["risks"].append(item)
        elif item_type in {"constraint", "assumption", "organization", "workforce"}:
            buckets["governance_objects"].append(item)
    buckets["scenarios"] = [_scenario_item(scenario) for scenario in getattr(decision, "scenarios", [])]
    buckets["observations"] = [_observation_item(record) for record in getattr(decision, "observation_records", [])]
    summary_counts = {key: len(value) for key, value in buckets.items()}
    return {
        "related_objects": {key: {"count": len(value), "items": value} for key, value in buckets.items()},
        "summary_counts": summary_counts,
        "impact": {
            "influenced_by": context_items,
            "influences": buckets["scenarios"] + buckets["observations"],
        },
    }
