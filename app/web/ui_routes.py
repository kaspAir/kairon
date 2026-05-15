from __future__ import annotations

import os
from dataclasses import dataclass

from flask import Blueprint, current_app, redirect, render_template, request, url_for

from app.domains.assessment.models import ImpactAssessment, RiskAssessment, SimulationRun
from app.domains.assessment.service import RiskAssessmentService
from app.domains.decision.models import Decision
from app.domains.decision.service import DecisionService
from app.domains.governance.models import ApprovalRecord, DecisionRecord
from app.domains.governance.service import GovernanceService
from app.domains.scenario.models import Scenario
from app.domains.scenario.service import ScenarioService
from app.domains.simulation.service import SimulationService
from app.shared.database import session_scope
from app.shared.errors import NotFoundError

bp = Blueprint("ui", __name__, url_prefix="/ui")


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


def _message() -> UiMessage | None:
    text = request.args.get("message")
    if not text:
        return None
    return UiMessage(level=request.args.get("level", "info"), text=text)


def _dashboard_summary(session) -> dict:
    decisions = session.query(Decision).all()
    high_risks = session.query(RiskAssessment).filter(RiskAssessment.severity == "high").count()
    recent_simulations = session.query(SimulationRun).order_by(SimulationRun.created_at.desc()).limit(5).all()
    pending_approvals = sum(1 for decision in decisions if decision.status in {"draft", "needs_review"})
    reassessments_needed = sum(1 for decision in decisions if decision.status == "needs_review") + high_risks
    return {
        "open_decisions": sum(1 for decision in decisions if decision.status in {"draft", "needs_review"}),
        "critical_risks": high_risks,
        "recent_simulations": len(recent_simulations),
        "pending_approvals": pending_approvals,
        "reassessments_needed": reassessments_needed,
        "environment": current_app.config.get("ENVIRONMENT", "development").upper(),
        "build_status": os.getenv("BUILD_STATUS", os.getenv("JENKINS_BUILD_STATUS", "not available")),
        "api_health": "ok",
    }


def _decision_or_404(session, decision_id: str) -> Decision:
    decision = session.get(Decision, decision_id)
    if decision is None:
        raise NotFoundError("Decision not found")
    return decision


def _latest_simulation(scenario: Scenario) -> SimulationRun | None:
    if not scenario.simulation_runs:
        return None
    return sorted(scenario.simulation_runs, key=lambda run: run.created_at, reverse=True)[0]


def _impact_for_scenario(scenario: Scenario) -> ImpactAssessment | None:
    latest_run = _latest_simulation(scenario)
    return latest_run.impact_assessment if latest_run and latest_run.impact_assessment else None


def _dominant_risk(decision: Decision) -> RiskAssessment | None:
    severity_rank = {"high": 3, "medium": 2, "low": 1}
    if not decision.risk_assessments:
        return None
    return sorted(decision.risk_assessments, key=lambda risk: severity_rank.get(risk.severity, 0), reverse=True)[0]


def _confidence_label(score: float | None) -> str:
    if score is None:
        return "low"
    if score >= 0.75:
        return "high"
    if score >= 0.5:
        return "medium"
    return "low"


def _comparison_rows(decision: Decision) -> list[dict]:
    rows = []
    dominant_risk = _dominant_risk(decision)
    scenarios_by_variant = {}
    for scenario in decision.scenarios:
        scenarios_by_variant.setdefault(scenario.variant_id, []).append(scenario)

    for variant in decision.variants:
        scenarios = scenarios_by_variant.get(variant.id) or [None]
        for scenario in scenarios:
            latest_run = _latest_simulation(scenario) if scenario else None
            impact = latest_run.impact_assessment if latest_run and latest_run.impact_assessment else None
            confidence_score = float(impact.confidence_score) if impact else None
            rows.append({
                "variant": variant,
                "scenario": scenario,
                "simulation": latest_run,
                "impact": impact,
                "risk": dominant_risk,
                "confidence": _confidence_label(confidence_score),
                "confidence_score": confidence_score,
                "governance_status": decision.status,
            })
    return rows


def _workspace_view_model(decision: Decision) -> dict:
    rows = _comparison_rows(decision)
    latest_record = sorted(decision.decision_records, key=lambda record: record.created_at, reverse=True)[0] if decision.decision_records else None
    return {
        "decision": decision,
        "comparison_rows": rows,
        "latest_record": latest_record,
        "dominant_risk": _dominant_risk(decision),
        "has_simulations": any(row["simulation"] for row in rows),
        "has_impacts": any(row["impact"] for row in rows),
    }


@bp.get("")
@bp.get("/")
def home():
    with session_scope() as session:
        decisions = session.query(Decision).order_by(Decision.created_at.desc()).all()
        return render_template(
            "dashboard.html",
            active_nav="decisions",
            decisions=decisions,
            summary=_dashboard_summary(session),
            message=_message(),
        )


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
            RiskAssessmentService(session).create_risk_assessment(
                decision_id=decision_id,
                summary=request.form.get("summary", ""),
                severity=request.form.get("severity", "medium"),
                mitigation=request.form.get("mitigation") or None,
                created_by=_created_by(),
            )
        return redirect(url_for("ui.decision_detail", decision_id=decision_id, message="Risk assessment saved", level="success"))
    except ValueError as exc:
        return redirect(url_for("ui.decision_detail", decision_id=decision_id, message=str(exc), level="error"))


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


@bp.post("/decisions/<decision_id>/records")
def create_record(decision_id):
    with session_scope() as session:
        GovernanceService(session).create_decision_record(decision_id, created_by=_created_by())
    return redirect(url_for("ui.decision_record", decision_id=decision_id, message="Decision record generated", level="success"))
