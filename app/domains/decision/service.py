from app.domains.decision.models import Decision, DecisionVariant
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
        }
