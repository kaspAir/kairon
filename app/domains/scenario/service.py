from app.domains.decision.models import Decision, DecisionVariant
from app.domains.scenario.models import Scenario
from app.shared.errors import NotFoundError


class ScenarioService:
    def __init__(self, session):
        self.session = session

    def create_scenario(
        self,
        decision_id: str,
        variant_id: str,
        name: str,
        description: str | None = None,
        case_volume: int = 1,
        processing_minutes_per_case: float = 0,
        hourly_cost: float = 0,
        created_by: str = "system",
    ) -> Scenario:
        if self.session.get(Decision, decision_id) is None:
            raise NotFoundError("Decision not found")
        variant = self.session.get(DecisionVariant, variant_id)
        if variant is None or variant.decision_id != decision_id:
            raise NotFoundError("Variant not found for decision")
        if not name or not name.strip():
            raise ValueError("Scenario name is required")
        if case_volume < 0 or processing_minutes_per_case < 0 or hourly_cost < 0:
            raise ValueError("Scenario values must not be negative")
        scenario = Scenario(
            decision_id=decision_id,
            variant_id=variant_id,
            name=name.strip(),
            description=description,
            case_volume=case_volume,
            processing_minutes_per_case=processing_minutes_per_case,
            hourly_cost=hourly_cost,
            created_by=created_by,
        )
        self.session.add(scenario)
        self.session.flush()
        return scenario
