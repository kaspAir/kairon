from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class DecisionStatusDefinition:
    value: str
    label: str
    description: str


DRAFT = "draft"
IN_REVIEW = "in_review"
SIMULATED = "simulated"
RISK_REVIEWED = "risk_reviewed"
GOVERNANCE_REVIEWED = "governance_reviewed"
APPROVED = "approved"
ARCHIVED = "archived"
OBSERVED = "observed"
REASSESSMENT_NEEDED = "reassessment_needed"
REASSESSING = "reassessing"

DECISION_STATUS_DEFINITIONS: tuple[DecisionStatusDefinition, ...] = (
    DecisionStatusDefinition(DRAFT, "Draft", "Decision is being prepared."),
    DecisionStatusDefinition(IN_REVIEW, "In Review", "Decision basis is being reviewed."),
    DecisionStatusDefinition(SIMULATED, "Simulated", "At least one scenario has simulation evidence."),
    DecisionStatusDefinition(RISK_REVIEWED, "Risk Reviewed", "Risks and side effects have been assessed."),
    DecisionStatusDefinition(GOVERNANCE_REVIEWED, "Governance Reviewed", "Governance review is ready for approval."),
    DecisionStatusDefinition(APPROVED, "Approved", "Decision has been approved by accountable humans."),
    DecisionStatusDefinition(ARCHIVED, "Archived", "Decision is no longer active."),
    DecisionStatusDefinition(OBSERVED, "Observed", "Decision outcome has been observed after implementation."),
    DecisionStatusDefinition(REASSESSMENT_NEEDED, "Reassessment Needed", "Observed outcome indicates that reassessment may be needed."),
    DecisionStatusDefinition(REASSESSING, "Reassessing", "Decision is currently being reassessed."),
)

DECISION_STATUS_LABELS = {definition.value: definition.label for definition in DECISION_STATUS_DEFINITIONS}
VALID_DECISION_STATUSES = frozenset(DECISION_STATUS_LABELS)

ALLOWED_STATUS_TRANSITIONS: dict[str, tuple[str, ...]] = {
    DRAFT: (IN_REVIEW, ARCHIVED),
    IN_REVIEW: (DRAFT, SIMULATED, ARCHIVED),
    SIMULATED: (RISK_REVIEWED, IN_REVIEW, ARCHIVED),
    RISK_REVIEWED: (GOVERNANCE_REVIEWED, REASSESSMENT_NEEDED, ARCHIVED),
    GOVERNANCE_REVIEWED: (APPROVED, RISK_REVIEWED, ARCHIVED),
    APPROVED: (OBSERVED, ARCHIVED),
    OBSERVED: (REASSESSMENT_NEEDED, ARCHIVED),
    REASSESSMENT_NEEDED: (REASSESSING, ARCHIVED),
    REASSESSING: (IN_REVIEW, GOVERNANCE_REVIEWED, APPROVED, ARCHIVED),
    ARCHIVED: (),
}


def normalize_decision_status(status: str | None) -> str:
    normalized = (status or "").strip().lower().replace("-", "_").replace(" ", "_")
    if normalized not in VALID_DECISION_STATUSES:
        raise ValueError(f"Unknown decision status: {status}")
    return normalized


def allowed_next_statuses(current_status: str | None) -> tuple[str, ...]:
    current = normalize_decision_status(current_status or DRAFT)
    return ALLOWED_STATUS_TRANSITIONS.get(current, ())


def assert_transition_allowed(current_status: str | None, target_status: str | None) -> tuple[str, str]:
    current = normalize_decision_status(current_status or DRAFT)
    target = normalize_decision_status(target_status)
    if target == current:
        raise ValueError(f"Decision is already in status {DECISION_STATUS_LABELS[target]}")
    if target not in ALLOWED_STATUS_TRANSITIONS.get(current, ()):
        allowed = ", ".join(DECISION_STATUS_LABELS[status] for status in ALLOWED_STATUS_TRANSITIONS.get(current, ())) or "none"
        raise ValueError(
            f"Invalid decision status transition from {DECISION_STATUS_LABELS[current]} to {DECISION_STATUS_LABELS[target]}. "
            f"Allowed next statuses: {allowed}."
        )
    return current, target
