from app.domains.decision.models import Decision, DecisionVariant
from app.domains.decision.status import allowed_next_statuses, assert_transition_allowed
from app.shared.errors import NotFoundError


class DecisionService:
    def __init__(self, session):
        self.session = session

    def create_decision(self, title: str, context: str | None = None, created_by: str = "system") -> Decision:
        if not title or not title.strip():
            raise ValueError("Decision title is required")
        decision = Decision(title=title.strip(), context=context, created_by=created_by)
        self.session.add(decision)
        self.session.flush()
        return decision

    def create_variant(
        self,
        decision_id: str,
        name: str,
        description: str | None = None,
        estimated_cost: float = 0,
        expected_benefit: float = 0,
        created_by: str = "system",
    ) -> DecisionVariant:
        decision = self.session.get(Decision, decision_id)
        if decision is None:
            raise NotFoundError("Decision not found")
        if not name or not name.strip():
            raise ValueError("Variant name is required")
        variant = DecisionVariant(
            decision_id=decision_id,
            name=name.strip(),
            description=description,
            estimated_cost=estimated_cost,
            expected_benefit=expected_benefit,
            created_by=created_by,
        )
        self.session.add(variant)
        self.session.flush()
        return variant


    def change_decision_status(self, decision_id: str, target_status: str, changed_by: str = "system") -> tuple[Decision, str]:
        """Change a decision status through the controlled lifecycle.

        The method intentionally keeps the MVP lightweight: it validates transitions,
        updates the governance fields and increments the version. A dedicated audit
        event/decision-record entry can be attached here later without changing routes.
        """
        decision = self.session.get(Decision, decision_id)
        if decision is None:
            raise NotFoundError("Decision not found")

        previous_status, normalized_target = assert_transition_allowed(decision.status, target_status)
        decision.status = normalized_target
        decision.created_by = decision.created_by or changed_by or "system"
        decision.version = (decision.version or 1) + 1
        self.session.add(decision)
        self.session.flush()
        return decision, previous_status

    def allowed_next_statuses(self, decision: Decision) -> tuple[str, ...]:
        return allowed_next_statuses(decision.status)

    def get_decision_record_view(self, decision_id: str) -> dict:
        decision = self.session.get(Decision, decision_id)
        if decision is None:
            raise NotFoundError("Decision not found")
        return {
            "id": decision.id,
            "title": decision.title,
            "description": decision.context,
            "status": decision.status,
            "variants": [
                {
                    "id": v.id,
                    "name": v.name,
                    "estimated_cost": float(v.estimated_cost),
                    "expected_benefit": float(v.expected_benefit),
                }
                for v in decision.variants
            ],
            "scenarios": [
                {
                    "id": s.id,
                    "name": s.name,
                    "case_volume": s.case_volume,
                    "processing_minutes_per_case": float(s.processing_minutes_per_case),
                    "hourly_cost": float(s.hourly_cost),
                    "simulation_runs": [
                        {
                            "id": run.id,
                            "total_processing_hours": float(run.total_processing_hours),
                            "total_cost": float(run.total_cost),
                            "impact_assessment": None if run.impact_assessment is None else {
                                "cost_impact": float(run.impact_assessment.cost_impact),
                                "benefit_impact": float(run.impact_assessment.benefit_impact),
                                "net_impact": float(run.impact_assessment.net_impact),
                                "confidence_score": float(run.impact_assessment.confidence_score),
                            },
                        }
                        for run in s.simulation_runs
                    ],
                }
                for s in decision.scenarios
            ],
            "decision_records": [
                {"id": r.id, "record_text": r.record_text, "created_at": r.created_at.isoformat()}
                for r in decision.decision_records
            ],
            "observation_records": [
                {
                    "id": observation.id,
                    "expected_benefit": float(observation.expected_benefit),
                    "actual_benefit": float(observation.actual_benefit),
                    "expected_cost": float(observation.expected_cost),
                    "actual_cost": float(observation.actual_cost),
                    "expected_risks": observation.expected_risks,
                    "actual_risks": observation.actual_risks,
                    "comment": observation.comment,
                    "observed_at": observation.observed_at.isoformat(),
                    "status": observation.status,
                }
                for observation in decision.observation_records
            ],
        }
