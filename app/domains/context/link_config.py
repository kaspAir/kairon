from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ContextLinkType:
    """Configured cross-context link type.

    This is intentionally configuration only. KAIRON does not persist generic
    context links in this MVP step and does not introduce a graph engine here.
    """

    key: str
    label: str
    source_context_type: str
    target_context_type: str
    description: str
    bidirectional: bool = False
    active: bool = True

    def as_dict(self) -> dict[str, Any]:
        return {
            "key": self.key,
            "label": self.label,
            "source_context_type": self.source_context_type,
            "target_context_type": self.target_context_type,
            "description": self.description,
            "bidirectional": self.bidirectional,
            "active": self.active,
        }


SUPPORTED_CONTEXT_LINK_TYPES: tuple[ContextLinkType, ...] = (
    ContextLinkType("process_to_decision", "Process to Decision", "process", "decision", "Links a process context to a decision that uses it as decision support context.", True),
    ContextLinkType("process_to_risk", "Process to Risk", "process", "risk", "Prepares traceability between process contexts and structured risk contexts.", True),
    ContextLinkType("process_to_organization", "Process to Organization", "process", "organization", "Prepares traceability between process contexts and organization contexts.", True),
    ContextLinkType("process_to_role", "Process to Role", "process", "role", "Prepares traceability between process contexts and roles or functions.", True),
    ContextLinkType("process_to_metric", "Process to Metric", "process", "metric", "Prepares traceability between process contexts and metrics or KPIs.", True),
    ContextLinkType("process_to_policy", "Process to Policy", "process", "policy", "Prepares traceability between process contexts and policies or legal foundations.", True),
    ContextLinkType("process_to_scenario", "Process to Scenario", "process", "scenario", "Prepares traceability between process contexts and scenario variants.", True),
    ContextLinkType("process_to_capability", "Process to Capability", "process", "capability", "Prepares traceability between process contexts and business capabilities.", True),
    ContextLinkType("process_to_constraint", "Process to Constraint", "process", "constraint", "Prepares traceability between process contexts and constraints.", True),
)


def get_context_link_types() -> tuple[ContextLinkType, ...]:
    """Return supported context link types.

    This is a lightweight architectural contract for future cross-domain
    linking. It is deliberately not a database-backed relation model yet.
    """

    return SUPPORTED_CONTEXT_LINK_TYPES


def context_link_config_view_model() -> dict[str, Any]:
    link_types = [link_type.as_dict() for link_type in get_context_link_types()]
    return {
        "link_types": link_types,
        "active_link_types": [link_type for link_type in link_types if link_type["active"]],
    }
