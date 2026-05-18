from app.domains.decision.models import Decision
from app.domains.assessment.models import RiskAssessment
from app.shared.errors import NotFoundError


class RiskAssessmentService:
    def __init__(self, session):
        self.session = session

    def create_risk_assessment(
        self,
        decision_id: str,
        summary: str,
        severity: str = "medium",
        mitigation: str | None = None,
        created_by: str = "system",
    ) -> RiskAssessment:
        if self.session.get(Decision, decision_id) is None:
            raise NotFoundError("Decision not found")
        if not summary or not summary.strip():
            raise ValueError("Risk summary is required")
        if severity not in {"low", "medium", "high"}:
            raise ValueError("Severity must be low, medium or high")
        risk = RiskAssessment(decision_id=decision_id, summary=summary, severity=severity, mitigation=mitigation, created_by=created_by)
        self.session.add(risk)
        self.session.flush()
        return risk
