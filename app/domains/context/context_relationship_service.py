from __future__ import annotations

from typing import Any
from uuid import uuid4

from sqlalchemy.orm.attributes import flag_modified

from app.domains.context.context_relationship_config import get_relationship_type


RELATED_OBJECT_CATEGORIES: tuple[tuple[str, str, str, tuple[str, ...]], ...] = (
    ("processes", "Processes", "Related Processes", ("process",)),
    ("risks", "Risks", "Related Risks", ("risk",)),
    ("policies", "Policies", "Related Policies", ("policy",)),
    ("scenarios", "Scenarios", "Related Scenarios", ("scenario",)),
    ("observations", "Observations", "Related Observations", ("observation", "observations")),
    ("governance_objects", "Governance Objects", "Related Governance Objects", ("governance", "control", "role", "organization")),
)

_CATEGORY_BY_CONTEXT_TYPE = {
    context_type: category_key
    for category_key, _label, _title, context_types in RELATED_OBJECT_CATEGORIES
    for context_type in context_types
}


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
    flag_modified(context_object, "metadata_json")

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


def _object_label(obj: Any, fallback: str | None = None) -> str:
    return (
        getattr(obj, "name", None)
        or getattr(obj, "title", None)
        or getattr(obj, "approved_by", None)
        or getattr(obj, "comment", None)
        or fallback
        or str(getattr(obj, "id", "Unknown object"))
    )


def _context_object_item(context_object, *, relationship: dict[str, Any] | None = None, direction: str | None = None) -> dict[str, Any]:
    metadata = getattr(context_object, "metadata_json", None) or {}
    return {
        "id": str(context_object.id),
        "name": context_object.name,
        "description": context_object.description,
        "context_type": context_object.context_type,
        "type_label": context_object.context_type.replace("_", " ").title(),
        "owner": context_object.owner,
        "confidence": context_object.confidence,
        "source": context_object.source,
        "metadata": metadata,
        "relationship_label": (relationship or {}).get("label"),
        "relationship_reason": (relationship or {}).get("reason"),
        "relationship_confidence": (relationship or {}).get("confidence"),
        "relationship_type": (relationship or {}).get("type"),
        "direction": direction,
        "detail_url": None,
    }


def _generic_item(obj: Any, context_type: str, *, relationship: dict[str, Any] | None = None, direction: str | None = None) -> dict[str, Any]:
    return {
        "id": str(getattr(obj, "id", "")),
        "name": _object_label(obj, context_type.replace("_", " ").title()),
        "description": getattr(obj, "description", None) or getattr(obj, "comment", None),
        "context_type": context_type,
        "type_label": context_type.replace("_", " ").title(),
        "owner": getattr(obj, "owner", None) or getattr(obj, "created_by", None),
        "confidence": getattr(obj, "confidence", None),
        "source": getattr(obj, "source", None),
        "metadata": {},
        "relationship_label": (relationship or {}).get("label"),
        "relationship_reason": (relationship or {}).get("reason"),
        "relationship_confidence": (relationship or {}).get("confidence"),
        "relationship_type": (relationship or {}).get("type"),
        "direction": direction,
        "detail_url": None,
    }


def _empty_related_objects() -> dict[str, dict[str, Any]]:
    return {
        key: {
            "key": key,
            "label": label,
            "title": title,
            "count": 0,
            "items": [],
        }
        for key, label, title, _context_types in RELATED_OBJECT_CATEGORIES
    }


def _add_related_item(related_objects: dict[str, dict[str, Any]], item: dict[str, Any]) -> None:
    category_key = _CATEGORY_BY_CONTEXT_TYPE.get(item.get("context_type"), "governance_objects")
    category = related_objects.setdefault(
        category_key,
        {
            "key": category_key,
            "label": category_key.replace("_", " ").title(),
            "title": f"Related {category_key.replace('_', ' ').title()}",
            "count": 0,
            "items": [],
        },
    )
    if any(existing.get("id") == item.get("id") and existing.get("relationship_type") == item.get("relationship_type") for existing in category["items"]):
        return
    category["items"].append(item)
    category["count"] = len(category["items"])


def build_decision_relationship_awareness(decision, *, context_objects: list[Any] | None = None) -> dict[str, Any]:
    """Build a human-readable relationship awareness view for a Decision.

    The result intentionally uses business language. It exposes related objects and impact orientation,
    not technical graph terms.
    """
    context_objects = list(context_objects if context_objects is not None else getattr(decision, "context_objects", []))
    context_by_id = {str(context_object.id): context_object for context_object in context_objects}
    related_objects = _empty_related_objects()
    influenced_by: list[dict[str, Any]] = []
    influences: list[dict[str, Any]] = []

    for context_object in context_objects:
        source_item = _context_object_item(context_object, direction="influenced_by")
        _add_related_item(related_objects, source_item)
        influenced_by.append(source_item)

        for relationship in list_context_relationships(context_object):
            target_id = str(relationship.get("target_context_id") or "")
            target_type = relationship.get("target_context_type") or "context"
            target = context_by_id.get(target_id)
            if target is not None:
                target_item = _context_object_item(target, relationship=relationship, direction="influences")
            else:
                target_item = {
                    "id": target_id,
                    "name": relationship.get("target_label") or relationship.get("target_name") or target_id,
                    "description": relationship.get("reason"),
                    "context_type": target_type,
                    "type_label": target_type.replace("_", " ").title(),
                    "owner": None,
                    "confidence": relationship.get("confidence"),
                    "source": None,
                    "metadata": {},
                    "relationship_label": relationship.get("label"),
                    "relationship_reason": relationship.get("reason"),
                    "relationship_confidence": relationship.get("confidence"),
                    "relationship_type": relationship.get("type"),
                    "direction": "influences",
                    "detail_url": None,
                }
            _add_related_item(related_objects, target_item)
            influences.append(target_item)

    for scenario in getattr(decision, "scenarios", []) or []:
        item = _generic_item(scenario, "scenario", direction="influences")
        _add_related_item(related_objects, item)
        influences.append(item)

    for observation in getattr(decision, "observation_records", []) or []:
        item = _generic_item(observation, "observation", direction="influences")
        _add_related_item(related_objects, item)
        influences.append(item)

    for approval in getattr(decision, "approval_records", []) or []:
        item = _generic_item(approval, "governance", direction="influenced_by")
        _add_related_item(related_objects, item)
        influenced_by.append(item)

    return {
        "related_objects": related_objects,
        "impact": {
            "influenced_by": influenced_by,
            "influences": influences,
        },
        "summary_counts": {key: category["count"] for key, category in related_objects.items()},
        "total_related_objects": sum(category["count"] for category in related_objects.values()),
    }


def build_context_related_objects(context_object, *, all_context_objects: list[Any] | None = None) -> dict[str, Any]:
    all_context_objects = list(all_context_objects or [])
    context_by_id = {str(obj.id): obj for obj in all_context_objects}
    related_objects = _empty_related_objects()

    for relationship in list_context_relationships(context_object):
        target_id = str(relationship.get("target_context_id") or "")
        target = context_by_id.get(target_id)
        if target is not None:
            item = _context_object_item(target, relationship=relationship, direction="influences")
        else:
            target_type = relationship.get("target_context_type") or "context"
            item = {
                "id": target_id,
                "name": relationship.get("target_label") or relationship.get("target_name") or target_id,
                "description": relationship.get("reason"),
                "context_type": target_type,
                "type_label": target_type.replace("_", " ").title(),
                "owner": None,
                "confidence": relationship.get("confidence"),
                "source": None,
                "metadata": {},
                "relationship_label": relationship.get("label"),
                "relationship_reason": relationship.get("reason"),
                "relationship_confidence": relationship.get("confidence"),
                "relationship_type": relationship.get("type"),
                "direction": "influences",
                "detail_url": None,
            }
        _add_related_item(related_objects, item)

    return {
        "context_id": str(context_object.id),
        "related_objects": related_objects,
        "summary_counts": {key: category["count"] for key, category in related_objects.items()},
        "total_related_objects": sum(category["count"] for category in related_objects.values()),
    }


def detect_context_conflicts(relationships) -> list[dict[str, Any]]:
    return []
