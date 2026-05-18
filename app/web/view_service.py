from decimal import Decimal

from app.domains.decision.models import Decision
from app.domains.governance.service import GovernanceService
from app.shared.errors import NotFoundError


class DecisionUIService:
    """Builds read-only view models for the Jinja MVP UI.

    The UI layer must not contain business logic. Mutations still go through the
    existing domain services; this service only assembles presentation data.
    """

    def __init__(self, session):
        self.session = session

    def list_decisions(self) -> list[dict]:
        decisions = self.session.query(Decision).order_by(Decision.created_at.desc()).all()
        return [self._decision_summary(decision) for decision in decisions]

    def get_decision_detail(self, decision_id: str) -> dict:
        decision = self.session.get(Decision, decision_id)
        if decision is None:
            raise NotFoundError("Decision not found")
        return {
            "decision": self._decision_summary(decision),
            "variants": [self._variant(variant) for variant in decision.variants],
            "scenarios": [self._scenario(scenario) for scenario in decision.scenarios],
            "risk_assessments": [self._risk(risk) for risk in decision.risk_assessments],
            "approval_records": [self._approval(approval) for approval in decision.approval_records],
            "latest_record": self._latest_record(decision),
        }

    def get_compare_view(self, decision_id: str) -> dict:
        detail = self.get_decision_detail(decision_id)
        comparison_rows = []
        scenario_by_variant = {}
        for scenario in detail["scenarios"]:
            scenario_by_variant.setdefault(scenario["variant_id"], []).append(scenario)

        for variant in detail["variants"]:
            related_scenarios = scenario_by_variant.get(variant["id"], [])
            if not related_scenarios:
                comparison_rows.append({
                    "variant": variant,
                    "scenario": None,
                    "simulation_run": None,
                    "impact_assessment": None,
                })
                continue
            for scenario in related_scenarios:
                latest_run = scenario["simulation_runs"][-1] if scenario["simulation_runs"] else None
                impact = latest_run.get("impact_assessment") if latest_run else None
                comparison_rows.append({
                    "variant": variant,
                    "scenario": scenario,
                    "simulation_run": latest_run,
                    "impact_assessment": impact,
                })

        return {**detail, "comparison_rows": comparison_rows}

    def get_decision_record_view(self, decision_id: str) -> dict:
        decision = self.session.get(Decision, decision_id)
        if decision is None:
            raise NotFoundError("Decision not found")
        return GovernanceService(self.session).build_decision_record_data(decision)

    def _latest_record(self, decision: Decision) -> dict | None:
        if not decision.decision_records:
            return None
        record = sorted(decision.decision_records, key=lambda item: item.created_at)[-1]
        return {
            "id": record.id,
            "decision_id": record.decision_id,
            "record_text": record.record_text,
            "record_data": record.record_data,
            "created_at": self._iso(record.created_at),
            "created_by": record.created_by,
            "status": record.status,
            "version": record.version,
        }

    def _decision_summary(self, decision: Decision) -> dict:
        return {
            "id": decision.id,
            "title": decision.title,
            "description": decision.context,
            "status": decision.status,
            "created_at": self._iso(decision.created_at),
            "updated_at": self._iso(decision.updated_at),
            "created_by": decision.created_by,
            "version": decision.version,
        }

    def _variant(self, variant) -> dict:
        return {
            "id": variant.id,
            "decision_id": variant.decision_id,
            "name": variant.name,
            "description": variant.description,
            "estimated_cost": self._number(variant.estimated_cost),
            "expected_benefit": self._number(variant.expected_benefit),
            "status": variant.status,
            "created_by": variant.created_by,
            "version": variant.version,
        }

    def _scenario(self, scenario) -> dict:
        return {
            "id": scenario.id,
            "decision_id": scenario.decision_id,
            "variant_id": scenario.variant_id,
            "name": scenario.name,
            "description": scenario.description,
            "case_volume": scenario.case_volume,
            "processing_minutes_per_case": self._number(scenario.processing_minutes_per_case),
            "hourly_cost": self._number(scenario.hourly_cost),
            "status": scenario.status,
            "created_by": scenario.created_by,
            "version": scenario.version,
            "simulation_runs": [self._simulation_run(run) for run in scenario.simulation_runs],
        }

    def _simulation_run(self, run) -> dict:
        return {
            "id": run.id,
            "scenario_id": run.scenario_id,
            "total_processing_hours": self._number(run.total_processing_hours),
            "total_cost": self._number(run.total_cost),
            "deterministic_formula": run.deterministic_formula,
            "simulated_at": self._iso(run.simulated_at),
            "created_by": run.created_by,
            "status": run.status,
            "impact_assessment": self._impact(run.impact_assessment) if run.impact_assessment else None,
        }

    def _impact(self, impact) -> dict:
        return {
            "id": impact.id,
            "simulation_run_id": impact.simulation_run_id,
            "cost_impact": self._number(impact.cost_impact),
            "benefit_impact": self._number(impact.benefit_impact),
            "net_impact": self._number(impact.net_impact),
            "confidence_score": self._number(impact.confidence_score),
            "created_by": impact.created_by,
            "status": impact.status,
        }

    def _risk(self, risk) -> dict:
        return {
            "id": risk.id,
            "decision_id": risk.decision_id,
            "summary": risk.summary,
            "severity": risk.severity,
            "mitigation": risk.mitigation,
            "created_by": risk.created_by,
            "status": risk.status,
        }

    def _approval(self, approval) -> dict:
        return {
            "id": approval.id,
            "decision_id": approval.decision_id,
            "approved_by": approval.approved_by,
            "comment": approval.comment,
            "created_at": self._iso(approval.created_at),
            "created_by": approval.created_by,
            "status": approval.status,
            "version": approval.version,
        }

    @staticmethod
    def _iso(value):
        return None if value is None else value.isoformat()

    @staticmethod
    def _number(value):
        if isinstance(value, Decimal):
            return float(value)
        return value
