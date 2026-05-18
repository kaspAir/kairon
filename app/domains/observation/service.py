from datetime import datetime
from decimal import Decimal

from app.domains.decision.models import Decision
from app.domains.observation.models import ObservationRecord
from app.shared.errors import NotFoundError

OBSERVATION_STATUSES = {"observed", "reassessment_needed", "reassessing"}


def _as_float(value) -> float:
    if value is None:
        return 0.0
    if isinstance(value, Decimal):
        return float(value)
    return float(value)


def delta_indicator(expected: float, actual: float, inverse: bool = False) -> str:
    expected = _as_float(expected)
    actual = _as_float(actual)
    if actual == expected:
        return "unchanged"
    better = actual > expected
    if inverse:
        better = actual < expected
    return "better_than_expected" if better else "worse_than_expected"


class ObservationService:
    def __init__(self, session):
        self.session = session

    def create_observation_record(
        self,
        decision_id: str,
        expected_benefit: float,
        actual_benefit: float,
        expected_cost: float,
        actual_cost: float,
        expected_risks: str | None = None,
        actual_risks: str | None = None,
        comment: str | None = None,
        observed_at: datetime | None = None,
        created_by: str = "system",
    ) -> ObservationRecord:
        decision = self.session.get(Decision, decision_id)
        if decision is None:
            raise NotFoundError("Decision not found")
        observation = ObservationRecord(
            decision_id=decision_id,
            expected_benefit=expected_benefit,
            actual_benefit=actual_benefit,
            expected_cost=expected_cost,
            actual_cost=actual_cost,
            expected_risks=expected_risks,
            actual_risks=actual_risks,
            comment=comment,
            observed_at=observed_at or datetime.utcnow(),
            created_by=created_by,
            status="observed",
        )
        decision.status = "observed"
        if actual_cost > expected_cost or actual_benefit < expected_benefit:
            decision.status = "reassessment_needed"
            observation.status = "reassessment_needed"
        self.session.add(observation)
        self.session.flush()
        return observation

    def observation_view_model(self, observation: ObservationRecord) -> dict:
        return {
            "id": observation.id,
            "expected_benefit": _as_float(observation.expected_benefit),
            "actual_benefit": _as_float(observation.actual_benefit),
            "benefit_delta": delta_indicator(observation.expected_benefit, observation.actual_benefit),
            "expected_cost": _as_float(observation.expected_cost),
            "actual_cost": _as_float(observation.actual_cost),
            "cost_delta": delta_indicator(observation.expected_cost, observation.actual_cost, inverse=True),
            "expected_risks": observation.expected_risks,
            "actual_risks": observation.actual_risks,
            "risk_delta": "unchanged" if (observation.actual_risks or "").strip() == (observation.expected_risks or "").strip() else "worse_than_expected",
            "comment": observation.comment,
            "observed_at": observation.observed_at,
            "status": observation.status,
            "created_by": observation.created_by,
        }
