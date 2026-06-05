from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class ContextRelationshipType:
    key: str
    label: str
    source_context_type: str
    target_context_type: str
    description: str
    bidirectional: bool = False
    active: bool = True

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


_DEFAULT_RELATIONSHIP_TYPES: dict[str, ContextRelationshipType] = {
    "process_to_decision": ContextRelationshipType(
        key="process_to_decision",
        label="Process to Decision",
        source_context_type="process",
        target_context_type="decision",
        description="Links a process context to a decision.",
    ),
    "process_to_risk": ContextRelationshipType(
        key="process_to_risk",
        label="Process to Risk",
        source_context_type="process",
        target_context_type="risk",
        description="Links a process context to a risk context.",
    ),
    "process_to_organization": ContextRelationshipType(
        key="process_to_organization",
        label="Process to Organization",
        source_context_type="process",
        target_context_type="organization",
        description="Links a process context to an organization context.",
    ),
    "process_to_role": ContextRelationshipType(
        key="process_to_role",
        label="Process to Role",
        source_context_type="process",
        target_context_type="role",
        description="Links a process context to a role context.",
    ),
    "process_to_metric": ContextRelationshipType(
        key="process_to_metric",
        label="Process to Metric",
        source_context_type="process",
        target_context_type="metric",
        description="Links a process context to a metric context.",
    ),
    "process_to_policy": ContextRelationshipType(
        key="process_to_policy",
        label="Process to Policy",
        source_context_type="process",
        target_context_type="policy",
        description="Links a process context to a policy context.",
    ),
    "process_to_scenario": ContextRelationshipType(
        key="process_to_scenario",
        label="Process to Scenario",
        source_context_type="process",
        target_context_type="scenario",
        description="Links a process context to a scenario context.",
    ),
    "process_to_capability": ContextRelationshipType(
        key="process_to_capability",
        label="Process to Capability",
        source_context_type="process",
        target_context_type="capability",
        description="Links a process context to a capability context.",
    ),
    "process_to_constraint": ContextRelationshipType(
        key="process_to_constraint",
        label="Process to Constraint",
        source_context_type="process",
        target_context_type="constraint",
        description="Links a process context to a constraint context.",
    ),
    "risk_to_control": ContextRelationshipType(
        key="risk_to_control",
        label="Risk to Control",
        source_context_type="risk",
        target_context_type="control",
        description="Links a risk context to a control context.",
    ),
    "policy_to_process": ContextRelationshipType(
        key="policy_to_process",
        label="Policy to Process",
        source_context_type="policy",
        target_context_type="process",
        description="Links a policy context to a process context.",
    ),
    "scenario_to_process": ContextRelationshipType(
        key="scenario_to_process",
        label="Scenario to Process",
        source_context_type="scenario",
        target_context_type="process",
        description="Links a scenario context to a process context.",
    ),
    "decision_to_process": ContextRelationshipType(
        key="decision_to_process",
        label="Decision to Process",
        source_context_type="decision",
        target_context_type="process",
        description="Links a decision to a process context.",
    ),
    "assumption_to_scenario": ContextRelationshipType(
        key="assumption_to_scenario",
        label="Assumption to Scenario",
        source_context_type="assumption",
        target_context_type="scenario",
        description="Links an assumption context to a scenario context.",
    ),
    "decision_to_context": ContextRelationshipType(
        key="decision_to_context",
        label="Decision to Context",
        source_context_type="decision",
        target_context_type="context",
        description="Links a decision to any context object.",
    ),
}


def get_supported_relationship_types() -> dict[str, ContextRelationshipType]:
    return dict(_DEFAULT_RELATIONSHIP_TYPES)


def get_relationship_type(key: str | None) -> ContextRelationshipType | None:
    if not key:
        return None
    return _DEFAULT_RELATIONSHIP_TYPES.get(key)


def list_active_relationship_types() -> list[ContextRelationshipType]:
    return [
        relationship_type
        for relationship_type in _DEFAULT_RELATIONSHIP_TYPES.values()
        if relationship_type.active
    ]


def context_relationship_config_view_model() -> dict[str, object]:
    active_types = list_active_relationship_types()
    return {
        "active_relationship_types": [relationship_type.as_dict() for relationship_type in active_types],
        "relationship_type_count": len(active_types),
    }
