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

# Compatibility aliases for historic or governance-derived values that may still
# be present in existing demo/local data. They must never break UI rendering.
LEGACY_DECISION_STATUS_ALIASES: dict[str, str] = {
    "needs_review": REASSESSMENT_NEEDED,
    "review_needed": REASSESSMENT_NEEDED,
    "requires_review": REASSESSMENT_NEEDED,
    "review": IN_REVIEW,
}

DECISION_STATUS_LABELS.update({
    "needs_review": "Needs Review",
    "review_needed": "Needs Review",
    "requires_review": "Needs Review",
    "review": "In Review",
})

VALID_DECISION_STATUSES = frozenset(definition.value for definition in DECISION_STATUS_DEFINITIONS)

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
    """Return a valid lifecycle status for current and legacy values.

    Older demo/governance data may contain values such as ``needs_review`` that
    are not part of the controlled Decision lifecycle. UI rendering and dashboard
    aggregation must degrade gracefully for such values instead of raising a 400.
    """
    normalized = (status or "").strip().lower().replace("-", "_").replace(" ", "_")
    if normalized in VALID_DECISION_STATUSES:
        return normalized
    if normalized in LEGACY_DECISION_STATUS_ALIASES:
        return LEGACY_DECISION_STATUS_ALIASES[normalized]
    return REASSESSMENT_NEEDED


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
