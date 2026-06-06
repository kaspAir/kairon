from __future__ import annotations

TRANSLATIONS: dict[str, dict[str, str]] = {
    "en": {
        "decision_workspace.title": "Decision Workspace",
        "decision_workspace.story_header": "Decision Story Header",
        "decision_workspace.why_this_decision": "Why this decision?",
        "decision_workspace.context": "Decision Context",
        "decision_workspace.expected_future": "Expected Future",
        "decision_workspace.impact": "Impact",
        "decision_workspace.reassessment": "Reassessment",
        "decision_workspace.related_objects": "Related Objects",
        "decision_workspace.related_processes": "Related Processes",
        "decision_workspace.related_risks": "Related Risks",
        "decision_workspace.related_policies": "Related Policies",
        "decision_workspace.related_scenarios": "Related Scenarios",
        "decision_workspace.related_observations": "Related Observations",
        "decision_workspace.related_governance_objects": "Related Governance Objects",
        "decision_workspace.no_related_objects": "No related objects have been documented yet.",
        "decision_workspace.no_scenarios": "No scenarios or explicit future assumptions have been documented yet.",
        "decision_workspace.no_reassessment_defined": "No reassessment has been defined yet.",
        "decision_workspace.no_decision_rationale": "No decision rationale has been documented yet.",
        "decision_workspace.influenced_by": "This decision is influenced by",
        "decision_workspace.influences": "This decision influences",
        "decision_workspace.no_influenced_by": "No influencing context has been documented yet.",
        "decision_workspace.no_influences": "No influenced objects have been documented yet.",
        "decision_workspace.status": "Status",
        "decision_workspace.created_at": "Created at",
        "decision_workspace.review_date": "Review date",
        "decision_workspace.owner": "Owner",
        "decision_workspace.confidence": "Confidence",
        "decision_workspace.governance_status": "Governance status",
        "decision_workspace.scenarios_considered": "Scenarios considered",
        "decision_workspace.expected_impact": "Expected impact",
        "decision_workspace.assumptions": "Assumptions",
        "decision_workspace.observed_reality": "Observed reality",
        "decision_workspace.review_trigger": "Review trigger",
        "decision_workspace.count_suffix": "item(s)",
        "decision_workspace.open_compare": "Open compare",
        "decision_workspace.open_decision_record": "Decision Record",
        "decision_workspace.context_help": "Relevant context objects explain the circumstances, constraints and dependencies of this decision.",
        "decision_workspace.future_help": "Scenarios, assumptions and simulations describe the future that was expected or considered.",
        "decision_workspace.reassessment_help": "Decisions remain reviewable after approval. Observations and changing assumptions can trigger reassessment.",
    }
}


def translate(key: str, language: str = "en") -> str:
    return TRANSLATIONS.get(language, TRANSLATIONS["en"]).get(key, key)


def translation_keys(language: str = "en") -> dict[str, str]:
    return dict(TRANSLATIONS.get(language, TRANSLATIONS["en"]))
