from __future__ import annotations

import os
from dataclasses import dataclass
from decimal import Decimal

from sqlalchemy import text

from flask import Blueprint, current_app, redirect, render_template, request, url_for

from app.domains.assessment.models import RiskAssessment, SimulationRun
from app.demo.seed import DEMO_DECISION_TITLE, seed_golden_demo
from app.domains.context.context_relationship_config import list_active_relationship_types
from app.domains.context.process_config import get_process_taxonomy
from app.domains.context.risk_config import get_risk_taxonomy
from app.domains.context.context_relationship_service import summarize_context_relationships, build_decision_relationship_awareness
from app.domains.context.models import DecisionContextObject
from app.domains.context.service import DecisionContextService
from app.domains.context.types import CONTEXT_TYPE_LABELS, CONTEXT_TYPES, CONFIDENCE_VALUES
from app.domains.assessment.service import RiskAssessmentService
from app.domains.decision.models import Decision
from app.domains.decision.service import DecisionService
from app.domains.decision.status import DECISION_STATUS_LABELS, DECISION_STATUS_DEFINITIONS, allowed_next_statuses
from app.domains.governance.models import ApprovalRecord
from app.domains.governance.service import GovernanceService
from app.domains.observation.service import ObservationService
from app.domains.scenario.models import Scenario
from app.domains.scenario.service import ScenarioService
from app.domains.simulation.service import SimulationService
from app.shared.database import session_scope
from app.shared.errors import NotFoundError
from app.shared.i18n import translate

from app.domains.context.link_config import context_link_config_view_model

bp = Blueprint("ui", __name__, url_prefix="/ui")

STATUS_SEQUENCE = tuple(status.value for status in DECISION_STATUS_DEFINITIONS)


OVERVIEW_PAGES = {
    "scenarios": {
        "nav": "scenarios",
        "eyebrow": "Scenario Overview",
        "title": "Szenarien als prüfbare Entscheidungsräume",
        "text": "Szenarien machen Annahmen und Kontextvarianten vergleichbar. Im MVP werden sie pro Decision und Variante geführt und deterministisch simuliert.",
        "empty_title": "Noch keine Szenarien im Workspace",
        "empty_text": "Lege in einer Decision Varianten und Szenarien an, um Simulationen, Impact Assessments und Entscheidungsdeltas aufzubauen.",
    },
    "compare": {
        "nav": "compare",
        "eyebrow": "Compare Overview",
        "title": "Varianten und Szenarien vergleichbar machen",
        "text": "Compare ist der zentrale KAIRON-Bereich: Kosten, Nutzen, Risiken, Confidence, Simulation Status und Governance Status werden als Entscheidungsgrundlage gegenübergestellt.",
        "empty_title": "Noch keine Vergleichsgrundlagen",
        "empty_text": "Öffne eine Decision, lege Varianten und Szenarien an und starte Simulationen. Danach wird der Compare Workspace entscheidungsfähig.",
    },
    "governance": {
        "nav": "governance",
        "eyebrow": "Governance Overview",
        "title": "Entscheidungen nachvollziehbar prüfen und freigeben",
        "text": "Governance bündelt Risiken, Approvals und Decision Records. KI bleibt beratend; die Entscheidung bleibt menschlich verantwortet.",
        "empty_title": "Noch keine Governance-Arbeit offen",
        "empty_text": "Erfasse Risiken und Approval Records in einer Decision, um Freigaben und auditierbare Entscheidungsgrundlagen sichtbar zu machen.",
    },
    "analytics": {
        "nav": "analytics",
        "eyebrow": "Analytics Overview",
        "title": "Decision Intelligence Kennzahlen vorbereiten",
        "text": "Analytics bleibt im MVP bewusst leichtgewichtig. Relevante Signale entstehen aus Simulationen, Impact Assessments, Risiken und Governance-Zuständen.",
        "empty_title": "Analytics ist vorbereitet",
        "empty_text": "Sobald mehrere Decisions, Szenarien und Simulationen vorhanden sind, können Trends, Baselines und Targets sauber aufgebaut werden.",
    },
}


@dataclass(frozen=True)
class UiMessage:
    level: str
    text: str


def _created_by() -> str:
    return (request.form.get("created_by") or request.headers.get("X-Kairon-User") or "system").strip() or "system"


def _to_float(value, default=0.0) -> float:
    if value in (None, ""):
        return default
    return float(value)


def _to_int(value, default=0) -> int:
    if value in (None, ""):
        return default
    return int(value)


def _as_float(value) -> float:
    if value is None:
        return 0.0
    if isinstance(value, Decimal):
        return float(value)
    return float(value)


def _message() -> UiMessage | None:
    text = request.args.get("message")
    if not text:
        return None
    return UiMessage(level=request.args.get("level", "info"), text=text)


def _latest_simulation(scenario: Scenario | None) -> SimulationRun | None:
    if scenario is None or not scenario.simulation_runs:
        return None
    return sorted(scenario.simulation_runs, key=lambda run: run.created_at, reverse=True)[0]


def _dominant_risk(decision: Decision) -> RiskAssessment | None:
    severity_rank = {"critical": 4, "high": 3, "medium": 2, "low": 1}
    if not decision.risk_assessments:
        return None
    return sorted(decision.risk_assessments, key=lambda risk: severity_rank.get(risk.severity, 0), reverse=True)[0]



def _risk_contexts(decision: Decision) -> list:
    return [obj for obj in decision.context_objects if obj.context_type == "risk"]


def _process_contexts(decision: Decision) -> list:
    return [obj for obj in decision.context_objects if obj.context_type == "process"]


def _process_context_view_model(obj) -> dict:
    metadata = obj.metadata_json or {}
    return {
        "id": obj.id,
        "name": obj.name,
        "description": obj.description,
        "source": obj.source,
        "owner": obj.owner,
        "confidence": obj.confidence,
        "process_level": metadata.get("process_level"),
        "process_level_label": metadata.get("process_level_label"),
        "scope": metadata.get("scope"),
        "created_at": obj.created_at,
    }


def _risk_context_view_model(obj) -> dict:
    metadata = obj.metadata_json or {}
    return {
        "id": obj.id,
        "name": obj.name,
        "description": obj.description,
        "source": obj.source,
        "owner": obj.owner,
        "confidence": obj.confidence,
        "category": metadata.get("category"),
        "probability": metadata.get("probability"),
        "impact": metadata.get("impact"),
        "severity": metadata.get("severity", "medium"),
        "impact_area": metadata.get("impact_area"),
        "mitigation": metadata.get("mitigation"),
        "risk_owner": metadata.get("risk_owner") or obj.owner,
        "review_required": bool(metadata.get("review_required")),
        "created_at": obj.created_at,
    }

def _group_process_landscape_items(items: list[dict], process_taxonomy: dict) -> list[dict]:
    labels = {
        option["value"]: option["label"]
        for option in process_taxonomy.get("level_options", [])
    }
    grouped: dict[str, list[dict]] = {}
    for item in items:
        grouped.setdefault(item.get("process_level") or "unknown", []).append(item)

    ordered_groups = []
    for level in process_taxonomy.get("levels", []):
        if level in grouped:
            ordered_groups.append({
                "key": level,
                "label": labels.get(level, level.replace("_", " ").title()),
                "items": grouped[level],
            })
    for level, values in grouped.items():
        if level not in process_taxonomy.get("levels", []):
            ordered_groups.append({
                "key": level,
                "label": labels.get(level, level.replace("_", " ").title()),
                "items": values,
            })
    return ordered_groups


def _dominant_risk_context(decision: Decision) -> dict | None:
    severity_rank = {"critical": 4, "high": 3, "medium": 2, "low": 1}
    risks = [_risk_context_view_model(obj) for obj in _risk_contexts(decision)]
    if not risks:
        return None
    return sorted(risks, key=lambda risk: severity_rank.get(risk.get("severity"), 0), reverse=True)[0]


def _latest_approval(decision: Decision) -> ApprovalRecord | None:
    if not decision.approval_records:
        return None
    return sorted(decision.approval_records, key=lambda approval: approval.created_at, reverse=True)[0]


def _confidence_label(score: float | None) -> str:
    if score is None:
        return "low"
    if score >= 0.75:
        return "high"
    if score >= 0.5:
        return "medium"
    return "low"


def _decision_confidence(decision: Decision) -> str:
    scores = []
    for scenario in decision.scenarios:
        latest_run = _latest_simulation(scenario)
        if latest_run and latest_run.impact_assessment:
            scores.append(_as_float(latest_run.impact_assessment.confidence_score))
    if not scores:
        return "low"
    return _confidence_label(sum(scores) / len(scores))


def _risk_label(risk) -> str:
    if not risk:
        return "none"
    if isinstance(risk, dict):
        return risk.get("severity", "none")
    return risk.severity


def _governance_state(decision: Decision) -> str:
    if decision.status in {"observed", "reassessment_needed", "reassessing"}:
        return decision.status
    latest_approval = _latest_approval(decision)
    if latest_approval and latest_approval.status == "approved":
        return "approved"
    if latest_approval:
        return "governance_reviewed"
    if decision.risk_assessments or _risk_contexts(decision):
        return "risk_reviewed"
    if any(_latest_simulation(scenario) for scenario in decision.scenarios):
        return "simulated"
    if decision.variants or decision.scenarios:
        return "in_review"
    return decision.status or "draft"


def _pending_governance_state(decision: Decision) -> str:
    state = _governance_state(decision)
    if state == "reassessment_needed":
        return "Reassessment needed"
    if state == "reassessing":
        return "Reassessing"
    if state == "observed":
        return "Observed"
    if state == "approved":
        return "Approved"
    if state == "risk_reviewed":
        return "Approval pending"
    if state == "simulated":
        return "Risk review pending"
    if state == "in_review":
        return "Simulation pending"
    return "Decision setup pending"


def _status_transition_actions(decision: Decision) -> list[dict]:
    return [
        {
            "value": status,
            "label": DECISION_STATUS_LABELS.get(status, status.replace("_", " ").title()),
            "description": "Controlled lifecycle transition; audit/Decision Record linkage prepared.",
        }
        for status in allowed_next_statuses(decision.status)
    ]


def _decision_card_view_model(decision: Decision) -> dict:
    latest_runs = [_latest_simulation(scenario) for scenario in decision.scenarios]
    latest_runs = [run for run in latest_runs if run is not None]
    latest_run = sorted(latest_runs, key=lambda run: run.created_at, reverse=True)[0] if latest_runs else None
    dominant_risk = _dominant_risk_context(decision) or _dominant_risk(decision)
    governance_state = _governance_state(decision)
    return {
        "id": decision.id,
        "title": decision.title,
        "description": decision.context,
        "status": governance_state,
        "created_by": decision.created_by,
        "created_at": decision.created_at,
        "variant_count": len(decision.variants),
        "scenario_count": len(decision.scenarios),
        "risk_count": len(_risk_contexts(decision)) or len(decision.risk_assessments),
        "latest_simulation": latest_run,
        "latest_simulation_status": "simulated" if latest_run else "not_simulated",
        "confidence": _decision_confidence(decision),
        "dominant_risk": _dominant_risk_context(decision) or dominant_risk,
        "pending_governance_state": _pending_governance_state(decision),
        "allowed_status_transitions": _status_transition_actions(decision),
    }


def _dashboard_summary(session, decisions: list[Decision]) -> dict:
    critical_risks = sum(1 for decision in decisions for risk in _risk_contexts(decision) if (risk.metadata_json or {}).get("severity") == "critical")
    recent_simulations = session.query(SimulationRun).order_by(SimulationRun.created_at.desc()).limit(5).all()
    pending_approvals = sum(1 for decision in decisions if _governance_state(decision) != "approved")
    reassessments_needed = sum(1 for decision in decisions if (_dominant_risk_context(decision) or _dominant_risk(decision)) and _governance_state(decision) != "approved")
    return {
        "open_decisions": sum(1 for decision in decisions if _governance_state(decision) not in {"approved", "archived"}),
        "critical_risks": critical_risks,
        "recent_simulations": len(recent_simulations),
        "pending_approvals": pending_approvals,
        "reassessments_needed": reassessments_needed,
        "environment": current_app.config.get("ENVIRONMENT", "development").upper(),
        "build_status": os.getenv("BUILD_STATUS", os.getenv("JENKINS_BUILD_STATUS", "not available")),
        "api_health": "ok",
        "demo_available": any(decision.title == DEMO_DECISION_TITLE for decision in decisions),
    }


def _decision_or_404(session, decision_id: str) -> Decision:
    decision = session.get(Decision, decision_id)
    if decision is None:
        raise NotFoundError("Decision not found")
    return decision


def _comparison_rows(decision: Decision) -> list[dict]:
    rows = []
    dominant_risk = _dominant_risk_context(decision) or _dominant_risk(decision)
    scenarios_by_variant = {}
    for scenario in decision.scenarios:
        scenarios_by_variant.setdefault(scenario.variant_id, []).append(scenario)

    for variant in decision.variants:
        scenarios = scenarios_by_variant.get(variant.id) or [None]
        for scenario in scenarios:
            latest_run = _latest_simulation(scenario)
            impact = latest_run.impact_assessment if latest_run and latest_run.impact_assessment else None
            confidence_score = _as_float(impact.confidence_score) if impact else None
            estimated_cost = _as_float(variant.estimated_cost)
            expected_benefit = _as_float(variant.expected_benefit)
            rows.append({
                "variant": variant,
                "scenario": scenario,
                "estimated_cost": estimated_cost,
                "expected_benefit": expected_benefit,
                "benefit_delta": expected_benefit - estimated_cost,
                "simulation": latest_run,
                "simulation_status": "simulated" if latest_run else "draft",
                "impact": impact,
                "impact_delta": _as_float(impact.net_impact) if impact else None,
                "risk": dominant_risk,
                "risk_label": _risk_label(dominant_risk),
                "confidence": _confidence_label(confidence_score),
                "confidence_score": confidence_score,
                "governance_status": _governance_state(decision),
            })
    return rows


def _scenario_rows(decision: Decision) -> list[dict]:
    return [
        {
            "scenario": scenario,
            "variant": scenario.variant,
            "latest_simulation": _latest_simulation(scenario),
        }
        for scenario in decision.scenarios
    ]


def _context_object_view_model(obj) -> dict:
    return {
        "id": obj.id,
        "context_type": obj.context_type,
        "type_label": CONTEXT_TYPE_LABELS.get(obj.context_type, obj.context_type.replace("_", " ").title()),
        "name": obj.name,
        "description": obj.description,
        "source": obj.source,
        "owner": obj.owner,
        "confidence": obj.confidence,
        "scenario_id": obj.scenario_id,
        "valid_from": obj.valid_from,
        "valid_to": obj.valid_to,
        "metadata_json": obj.metadata_json or {},
    }


def _context_panels(decision: Decision) -> list[dict]:
    grouped = {context_type: [] for context_type in CONTEXT_TYPES}
    for obj in decision.context_objects:
        grouped.setdefault(obj.context_type, []).append(_context_object_view_model(obj))

    definitions = [
        ("process", "Process Context", "Prozessbezug der Decision", "Noch kein Prozesskontext verknüpft", "Erfasse Prozesslandkarte, Prozessversion, betroffene Prozessschritte oder BPMN-Referenzen als Kontext. Eine vollständige BPMN-Engine folgt bewusst später."),
        ("organization", "Organization Context", "Organisationseinheiten und Verantwortlichkeiten", "Noch kein Organisationskontext erfasst", "Erfasse betroffene Organisationseinheiten, Rollen, Verantwortlichkeiten oder Governance-Gremien. Ein Organigramm-Editor ist im MVP bewusst nicht enthalten."),
        ("workforce", "Resource / FTE Context", "Kapazität, Ressourcen und FTE-Wirkung", "Noch keine Ressourcen- oder FTE-Grundlage", "Erfasse FTE-Annahmen, Kapazitätsbezug oder Skill-/Rollenabhängigkeiten als strukturierte Entscheidungsgrundlage."),
        ("risk", "Risk Management", "Risiken, Unsicherheiten und Nebenwirkungen", "Noch keine Risiken bewertet", "Erfasse Risiken oder Unsicherheiten als Kontextobjekte. Das ergänzt Risk Assessments, ersetzt aber noch kein komplexes Risikomanagement."),
        ("constraint", "Constraint Context", "Rahmenbedingungen und Einschränkungen", "Noch keine Constraints erfasst", "Erfasse Budgetgrenzen, regulatorische Vorgaben, Kapazitätsgrenzen oder Vier-Augen-Prinzipien als entscheidungsrelevante Constraints."),
        ("cost", "Cost Context", "Kostenannahmen und Kostentreiber", "Noch kein Kostenkontext erfasst", "Erfasse Kostenquellen, Kostensätze oder Annahmen, damit spätere Simulationen belastbarer werden."),
        ("metric", "Metric Context", "Kennzahlen und Zielgrössen", "Noch keine Metriken verknüpft", "Erfasse KPIs, Baselines oder Targets, die für die Bewertung dieser Decision relevant sind."),
        ("assumption", "Assumption Context", "Annahmen und Schätzwerte", "Noch keine Annahmen erfasst", "Erfasse explizite Annahmen mit Quelle, Owner und Confidence. Später können daraus Assumption Sets entstehen."),
        ("external_factor", "External Factor Context", "Externe Einflussfaktoren", "Noch keine externen Faktoren erfasst", "Erfasse Markt-, Lieferanten-, Rechts- oder Technologieeinflüsse, die die Entscheidung verändern können."),
    ]
    return [
        {
            "key": f"context-{context_type}",
            "context_type": context_type,
            "title": title,
            "summary": summary,
            "items": grouped.get(context_type, []),
            "empty_title": empty_title,
            "empty_text": empty_text,
            "prepared_for": CONTEXT_TYPE_LABELS.get(context_type, context_type),
        }
        for context_type, title, summary, empty_title, empty_text in definitions
    ]


def _context_summary(decision: Decision) -> dict:
    counts = {context_type: 0 for context_type in CONTEXT_TYPES}
    for obj in decision.context_objects:
        counts[obj.context_type] = counts.get(obj.context_type, 0) + 1
    return {
        "total": len(decision.context_objects),
        "counts": counts,
        "type_options": [(context_type, CONTEXT_TYPE_LABELS[context_type]) for context_type in CONTEXT_TYPES],
        "confidence_options": CONFIDENCE_VALUES,
        "risk_taxonomy": get_risk_taxonomy().as_dict(),
        "process_taxonomy": get_process_taxonomy().as_dict(),
    }

def _observation_records(decision: Decision) -> list[dict]:
    service = ObservationService(None)
    return [service.observation_view_model(record) for record in sorted(decision.observation_records, key=lambda record: record.observed_at, reverse=True)]


def _observation_context(decision: Decision) -> dict:
    observations = _observation_records(decision)
    latest = observations[0] if observations else None
    return {
        "records": observations,
        "latest": latest,
        "status": decision.status if decision.status in {"observed", "reassessment_needed", "reassessing"} else (latest["status"] if latest else "not_observed"),
        "empty_title": "Noch keine Beobachtung erfasst",
        "empty_text": "Beobachtungen machen Entscheidungen überprüfbar: Erwarteter Nutzen, tatsächlicher Nutzen, Kosten und Risiken werden nachverfolgt, damit KAIRON später Reassessments auslösen kann.",
    }



def _decision_workspace_header(decision: Decision) -> dict:
    metadata = getattr(decision, "metadata_json", None) or {}
    return {
        "title": decision.title,
        "status": decision.status,
        "created_at": decision.created_at,
        "decided_at": metadata.get("decided_at"),
        "review_date": metadata.get("review_date") or metadata.get("reassessment_date"),
        "owner": metadata.get("owner") or metadata.get("responsible_person") or metadata.get("responsible_role") or decision.created_by,
        "confidence": _decision_confidence(decision),
        "governance_status": _governance_state(decision),
    }


def _expected_future(decision: Decision, rows: list[dict]) -> dict:
    assumptions = [
        _context_object_view_model(obj)
        for obj in decision.context_objects
        if obj.context_type == "assumption"
    ]
    impact_rows = [row for row in rows if row.get("impact")]
    return {
        "scenarios": _scenario_rows(decision),
        "assumptions": assumptions,
        "impact_rows": impact_rows,
        "has_expected_future": bool(decision.scenarios or assumptions or impact_rows),
    }


def _reassessment_workspace(decision: Decision) -> dict:
    metadata = getattr(decision, "metadata_json", None) or {}
    observations = _observation_records(decision)
    assumptions_to_review = [
        _context_object_view_model(obj)
        for obj in decision.context_objects
        if obj.context_type == "assumption" and (obj.metadata_json or {}).get("review_required")
    ]
    return {
        "review_date": metadata.get("review_date") or metadata.get("reassessment_date"),
        "assumptions_to_review": assumptions_to_review,
        "observations": observations,
        "latest_observation": observations[0] if observations else None,
        "has_reassessment": bool(metadata.get("review_date") or metadata.get("reassessment_date") or assumptions_to_review or observations),
    }

def _workspace_view_model(decision: Decision) -> dict:
    rows = _comparison_rows(decision)
    latest_record = sorted(decision.decision_records, key=lambda record: record.created_at, reverse=True)[0] if decision.decision_records else None
    relationship_awareness = build_decision_relationship_awareness(decision)
    return {
        "decision": decision,
        "decision_card": _decision_card_view_model(decision),
        "context_panels": _context_panels(decision),
        "context_summary": _context_summary(decision),
        "observation_context": _observation_context(decision),
        "comparison_rows": rows,
        "scenario_rows": _scenario_rows(decision),
        "latest_record": latest_record,
        "dominant_risk": _dominant_risk_context(decision) or _dominant_risk(decision),
        "risk_contexts": [_risk_context_view_model(obj) for obj in _risk_contexts(decision)],
        "process_contexts": [_process_context_view_model(obj) for obj in _process_contexts(decision)],
        "process_taxonomy": get_process_taxonomy().as_dict(),
        "governance_status": _governance_state(decision),
        "status_sequence": STATUS_SEQUENCE,
        "status_labels": DECISION_STATUS_LABELS,
        "status_transition_actions": _status_transition_actions(decision),
        "has_simulations": any(row["simulation"] for row in rows),
        "has_impacts": any(row["impact"] for row in rows),
        "relationship_awareness": relationship_awareness,
        "decision_workspace_header": _decision_workspace_header(decision),
        "expected_future": _expected_future(decision, rows),
        "reassessment_workspace": _reassessment_workspace(decision),
<<<<<<< Updated upstream
=======
        "t": translate,
>>>>>>> Stashed changes
    }


@bp.get("")
@bp.get("/")
def home():
    with session_scope() as session:
        decisions = session.query(Decision).order_by(Decision.created_at.desc()).all()
        decision_cards = [_decision_card_view_model(decision) for decision in decisions]
        return render_template(
            "dashboard.html",
            active_nav="decisions",
            decisions=decision_cards,
            summary=_dashboard_summary(session, decisions),
            status_sequence=STATUS_SEQUENCE,
            message=_message(),
        )



@bp.post("/demo-seed")
def load_demo_seed():
    with session_scope() as session:
        decision = seed_golden_demo(session)
        return redirect(url_for(
            "ui.decision_detail",
            decision_id=decision.id,
            message="Golden demo data loaded",
            level="success",
        ))


def _render_overview(section: str):
    page = OVERVIEW_PAGES.get(section)
    if page is None:
        raise NotFoundError("Workspace section not found")
    with session_scope() as session:
        decisions = session.query(Decision).order_by(Decision.created_at.desc()).all()
        return render_template(
            "overview.html",
            active_nav=page["nav"],
            page=page,
            decisions=[_decision_card_view_model(decision) for decision in decisions],
            summary=_dashboard_summary(session, decisions),
            message=_message(),
        )


@bp.get("/scenarios")
def scenarios_overview():
    return _render_overview("scenarios")


@bp.get("/compare")
def compare_overview():
    return _render_overview("compare")


@bp.get("/governance")
def governance_overview():
    return _render_overview("governance")


@bp.get("/analytics")
def analytics_overview():
    return _render_overview("analytics")


@bp.get("/<section>")
def overview(section):
    return _render_overview(section)


def _db_status(session) -> str:
    try:
        session.execute(text("select 1"))
        return "ok"
    except Exception:
        current_app.logger.exception("database status check failed")
        return "error"




@bp.get("/risk-taxonomy")
def risk_taxonomy():
    risk_taxonomy = get_risk_taxonomy().as_dict()
    return render_template(
        "risk_taxonomy.html",
        active_nav="governance",
        message=_message(),
        risk_taxonomy=risk_taxonomy,
    )


@bp.get("/taxonomy")
def taxonomy_alias():
    return risk_taxonomy()


@bp.get("/process-taxonomy")
def process_taxonomy():
    process_taxonomy = get_process_taxonomy().as_dict()
    return render_template(
        "process_taxonomy.html",
        active_nav="governance",
        message=_message(),
        process_taxonomy=process_taxonomy,
    )


@bp.get("/processes/taxonomy")
def process_taxonomy_alias():
    return process_taxonomy()


@bp.get("/system-status")
def system_status():
    with session_scope() as session:
        api_health = "ok"
        db_status = _db_status(session)
        status = {
            "environment": current_app.config.get("ENVIRONMENT", "development").upper(),
            "api_health": api_health,
            "db_status": db_status,
            "build_status": os.getenv("BUILD_STATUS", os.getenv("JENKINS_BUILD_STATUS", "not available")),
            "pipeline_hint": "Pipeline from SCM should run against the checked-out branch. /api is the official API path; /health remains the smoke-test endpoint.",
        }
        return render_template("system_status.html", active_nav="system", status=status, message=_message())


@bp.post("/decisions")
def create_decision():
    try:
        with session_scope() as session:
            decision = DecisionService(session).create_decision(
                title=request.form.get("title", ""),
                context=request.form.get("description") or None,
                created_by=_created_by(),
            )
            return redirect(url_for("ui.decision_detail", decision_id=decision.id))
    except ValueError as exc:
        return redirect(url_for("ui.home", message=str(exc), level="error"))


@bp.get("/decisions/<decision_id>")
def decision_detail(decision_id):
    with session_scope() as session:
        decision = _decision_or_404(session, decision_id)
        return render_template(
            "decisions/detail.html",
            active_nav="decisions",
            message=_message(),
            **_workspace_view_model(decision),
        )


@bp.get("/decisions/<decision_id>/compare")
def decision_compare(decision_id):
    with session_scope() as session:
        decision = _decision_or_404(session, decision_id)
        return render_template(
            "decisions/compare.html",
            active_nav="compare",
            message=_message(),
            **_workspace_view_model(decision),
        )


@bp.get("/decisions/<decision_id>/record")
def decision_record(decision_id):
    with session_scope() as session:
        decision = _decision_or_404(session, decision_id)
        return render_template(
            "decisions/record.html",
            active_nav="governance",
            message=_message(),
            **_workspace_view_model(decision),
        )


@bp.post("/decisions/<decision_id>/status")
def change_decision_status(decision_id):
    target_status = request.form.get("status", "")
    try:
        with session_scope() as session:
            decision, previous_status = DecisionService(session).change_decision_status(
                decision_id=decision_id,
                target_status=target_status,
                changed_by=_created_by(),
            )
            label = DECISION_STATUS_LABELS.get(decision.status, decision.status.replace("_", " ").title())
            return redirect(url_for("ui.decision_detail", decision_id=decision.id, message=f"Status changed to {label}", level="success") + "#lifecycle")
    except ValueError as exc:
        return redirect(url_for("ui.decision_detail", decision_id=decision_id, message=str(exc), level="error") + "#lifecycle")


@bp.post("/decisions/<decision_id>/context-objects")
def create_context_object(decision_id):
    try:
        with session_scope() as session:
            DecisionContextService(session).create_context_object(
                decision_id=decision_id,
                context_type=request.form.get("context_type", ""),
                scenario_id=request.form.get("scenario_id") or None,
                name=request.form.get("name", ""),
                description=request.form.get("description") or None,
                source=request.form.get("source") or None,
                owner=request.form.get("owner") or None,
                confidence=request.form.get("confidence", "medium"),
            )
        return redirect(url_for("ui.decision_detail", decision_id=decision_id, message="Context object saved", level="success") + "#context")
    except ValueError as exc:
        return redirect(url_for("ui.decision_detail", decision_id=decision_id, message=str(exc), level="error") + "#context")


@bp.post("/decisions/<decision_id>/process-contexts")
def create_process_context(decision_id):
    try:
        with session_scope() as session:
            DecisionContextService(session).create_process_context(
                decision_id=decision_id,
                name=request.form.get("name", ""),
                description=request.form.get("description") or None,
                process_level=request.form.get("process_level") or None,
                owner=request.form.get("owner") or None,
                scope=request.form.get("scope") or None,
                source=request.form.get("source") or None,
                confidence=request.form.get("confidence", "medium"),
                created_by=_created_by(),
            )
        return redirect(
            url_for(
                "ui.decision_detail",
                decision_id=decision_id,
                message="Process context saved",
                level="success",
            ) + "#process-context"
        )
    except ValueError as exc:
        return redirect(
            url_for("ui.decision_detail", decision_id=decision_id, message=str(exc), level="error") + "#process-context"
        )


@bp.post("/decisions/<decision_id>/variants")
def create_variant(decision_id):
    try:
        with session_scope() as session:
            DecisionService(session).create_variant(
                decision_id=decision_id,
                name=request.form.get("name", ""),
                description=request.form.get("description") or None,
                estimated_cost=_to_float(request.form.get("estimated_cost")),
                expected_benefit=_to_float(request.form.get("expected_benefit")),
                created_by=_created_by(),
            )
        return redirect(url_for("ui.decision_detail", decision_id=decision_id, message="Variant created", level="success"))
    except ValueError as exc:
        return redirect(url_for("ui.decision_detail", decision_id=decision_id, message=str(exc), level="error"))


@bp.post("/decisions/<decision_id>/scenarios")
def create_scenario(decision_id):
    try:
        with session_scope() as session:
            ScenarioService(session).create_scenario(
                decision_id=decision_id,
                variant_id=request.form.get("variant_id", ""),
                name=request.form.get("name", ""),
                description=request.form.get("description") or None,
                case_volume=_to_int(request.form.get("case_volume"), 1),
                processing_minutes_per_case=_to_float(request.form.get("processing_minutes_per_case")),
                hourly_cost=_to_float(request.form.get("hourly_cost")),
                created_by=_created_by(),
            )
        return redirect(url_for("ui.decision_detail", decision_id=decision_id, message="Scenario created", level="success"))
    except ValueError as exc:
        return redirect(url_for("ui.decision_detail", decision_id=decision_id, message=str(exc), level="error"))


@bp.post("/scenarios/<scenario_id>/simulate")
def simulate_scenario(scenario_id):
    with session_scope() as session:
        scenario = session.get(Scenario, scenario_id)
        if scenario is None:
            raise NotFoundError("Scenario not found")
        decision_id = scenario.decision_id
        SimulationService(session).run_deterministic_simulation(scenario_id, created_by=_created_by())
    return redirect(url_for("ui.decision_compare", decision_id=decision_id, message="Simulation completed", level="success"))


@bp.post("/decisions/<decision_id>/risks")
def create_risk(decision_id):
    try:
        with session_scope() as session:
            DecisionContextService(session).create_risk_context(
                decision_id=decision_id,
                name=request.form.get("name") or request.form.get("summary"),
                summary=request.form.get("summary") or request.form.get("name"),
                description=request.form.get("description") or None,
                category=request.form.get("category") or None,
                probability=request.form.get("probability") or None,
                impact=request.form.get("impact") or None,
                severity=request.form.get("severity") or None,
                impact_area=request.form.get("impact_area") or None,
                mitigation=request.form.get("mitigation") or None,
                risk_owner=request.form.get("risk_owner") or None,
                review_required=request.form.get("review_required") == "on",
                source=request.form.get("source") or None,
                owner=request.form.get("owner") or request.form.get("risk_owner") or None,
                confidence=request.form.get("confidence", "medium"),
            )
        return redirect(url_for("ui.decision_detail", decision_id=decision_id, message="Risk context saved", level="success") + "#risks")
    except ValueError as exc:
        return redirect(url_for("ui.decision_detail", decision_id=decision_id, message=str(exc), level="error") + "#risks")


@bp.post("/decisions/<decision_id>/approvals")
def create_approval(decision_id):
    try:
        with session_scope() as session:
            GovernanceService(session).create_approval_record(
                decision_id=decision_id,
                approved_by=request.form.get("approved_by", ""),
                status=request.form.get("status", "approved"),
                comment=request.form.get("comment") or None,
                created_by=_created_by(),
            )
        return redirect(url_for("ui.decision_detail", decision_id=decision_id, message="Governance state updated", level="success"))
    except ValueError as exc:
        return redirect(url_for("ui.decision_detail", decision_id=decision_id, message=str(exc), level="error"))


@bp.post("/decisions/<decision_id>/observations")
def create_observation(decision_id):
    try:
        with session_scope() as session:
            ObservationService(session).create_observation_record(
                decision_id=decision_id,
                expected_benefit=_to_float(request.form.get("expected_benefit")),
                actual_benefit=_to_float(request.form.get("actual_benefit")),
                expected_cost=_to_float(request.form.get("expected_cost")),
                actual_cost=_to_float(request.form.get("actual_cost")),
                expected_risks=request.form.get("expected_risks") or None,
                actual_risks=request.form.get("actual_risks") or None,
                comment=request.form.get("comment") or None,
                created_by=_created_by(),
            )
        return redirect(url_for("ui.decision_detail", decision_id=decision_id, message="Observation saved", level="success") + "#observation")
    except ValueError as exc:
        return redirect(url_for("ui.decision_detail", decision_id=decision_id, message=str(exc), level="error"))


@bp.post("/decisions/<decision_id>/records")
def create_record(decision_id):
    with session_scope() as session:
        GovernanceService(session).create_decision_record(decision_id, created_by=_created_by())
    return redirect(url_for("ui.decision_record", decision_id=decision_id, message="Decision record generated", level="success"))


@bp.get("/context-relationships")
def context_relationships():
    with session_scope() as session:
        all_context_objects = (
            session.query(DecisionContextObject)
            .order_by(DecisionContextObject.context_type.asc(), DecisionContextObject.created_at.desc())
            .all()
        )
        return render_template(
            "context_relationships.html",
            active_nav="processes",
            message=_message(),
            relationship_types=[
                relationship_type.as_dict()
                for relationship_type in list_active_relationship_types()
            ],
            relationship_summary=summarize_context_relationships(all_context_objects),
        )

@bp.get("/process-landscape")
def process_landscape():
    with session_scope() as session:
        service = DecisionContextService(session)
        process_taxonomy = get_process_taxonomy().as_dict()
        items = service.process_landscape_items()
        return render_template(
            "process_landscape.html",
            active_nav="processes",
            message=_message(),
            process_taxonomy=process_taxonomy,
            process_landscape_items=items,
            grouped_process_contexts=_group_process_landscape_items(items, process_taxonomy),
            context_link_config=context_link_config_view_model(),
        )

