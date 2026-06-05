from __future__ import annotations

from typing import Any
from uuid import uuid4

from app.domains.context.context_relationship_config import get_relationship_type


def _metadata(context_object) -> dict[str, Any]:
    metadata = getattr(context_object, "metadata_json", None)
    if not isinstance(metadata, dict):
        metadata = {}
    context_object.metadata_json = metadata
    return metadata


def _relationships(context_object) -> list[dict[str, Any]]:
    metadata = _metadata(context_object)
    relationships = metadata.get("relationships")
    if not isinstance(relationships, list):
        relationships = []
        metadata["relationships"] = relationships
    return relationships


def add_context_relationship(
    context_object,
    *,
    relationship_type: str,
    target_context_id: str,
    target_context_type: str | None = None,
    label: str | None = None,
    reason: str | None = None,
    confidence: str | None = None,
    extra: dict[str, Any] | None = None,
) -> dict[str, Any]:
    configured_type = get_relationship_type(relationship_type)
    if configured_type is None or not configured_type.active:
        raise ValueError(f"Unsupported or inactive relationship type: {relationship_type}")

    target_id = str(target_context_id or "").strip()
    if not target_id:
        raise ValueError("target_context_id is required")

    relationship = {
        "id": str(uuid4()),
        "type": relationship_type,
        "target_context_id": target_id,
        "target_context_type": target_context_type or configured_type.target_context_type,
        "label": label or configured_type.label,
        "reason": reason,
        "confidence": confidence,
    }

    if extra and isinstance(extra, dict):
        relationship.update(extra)

    relationships = _relationships(context_object)
    relationships.append(relationship)

    metadata = _metadata(context_object)
    metadata["relationships"] = relationships
    context_object.metadata_json = dict(metadata)

    return relationship


def list_context_relationships(context_object) -> list[dict[str, Any]]:
    return list(_relationships(context_object))


def count_context_relationships(context_object) -> int:
    return len(list_context_relationships(context_object))


def summarize_context_relationships(context_objects) -> list[dict[str, Any]]:
    summary = []
    for context_object in context_objects:
        relationships = list_context_relationships(context_object)
        if not relationships:
            continue
        summary.append(
            {
                "context_id": str(context_object.id),
                "decision_id": str(context_object.decision_id),
                "context_type": context_object.context_type,
                "name": context_object.name,
                "relationship_count": len(relationships),
                "relationships": relationships,
            }
        )
    return summary


def detect_context_conflicts(relationships) -> list[dict[str, Any]]:
    return []
