from app.domains.decision.models import Decision
from app.domains.decision.status import APPROVED, IN_REVIEW, REASSESSMENT_NEEDED
from app.domains.governance.models import ApprovalRecord, DecisionRecord
from app.shared.errors import NotFoundError


def _decision_status_for_approval_status(status: str) -> str:
    if status == "approved":
        return APPROVED
    if status == "needs_review":
        return REASSESSMENT_NEEDED
    if status == "rejected":
        return IN_REVIEW
    return IN_REVIEW


class GovernanceService:
    def __init__(self, session):
        self.session = session

    def create_approval_record(
        self,
        decision_id: str,
        approved_by: str,
        status: str = "approved",
        comment: str | None = None,
        created_by: str = "system",
    ) -> ApprovalRecord:
        decision = self.session.get(Decision, decision_id)
        if decision is None:
            raise NotFoundError("Decision not found")
        if status not in {"approved", "rejected", "needs_review"}:
            raise ValueError("Invalid approval status")
        if not approved_by or not approved_by.strip():
            raise ValueError("approved_by is required")
        approval = ApprovalRecord(decision_id=decision_id, approved_by=approved_by.strip(), status=status, comment=comment, created_by=created_by)
        decision.status = _decision_status_for_approval_status(status)
        self.session.add(approval)
        self.session.flush()
        return approval

    def create_decision_record(self, decision_id: str, created_by: str = "system") -> DecisionRecord:
        decision = self.session.get(Decision, decision_id)
        if decision is None:
            raise NotFoundError("Decision not found")
        text = f"Decision '{decision.title}' recorded with status '{decision.status}'. AI advisory did not make this decision."
        record = DecisionRecord(decision_id=decision_id, record_text=text, created_by=created_by)
        self.session.add(record)
        self.session.flush()
        return record
