from __future__ import annotations

from typing import Any
from uuid import uuid4

from sqlalchemy.orm.attributes import flag_modified

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


def detect_context_conflicts(relationships) -> list[dict[str, Any]]:
    return []

<<<<<<< Updated upstream
_RELATED_OBJECT_CATEGORIES = {
    "process": ("processes", "Related Processes"),
    "risk": ("risks", "Related Risks"),
    "policy": ("policies", "Related Policies"),
    "scenario": ("scenarios", "Related Scenarios"),
    "observation": ("observations", "Related Observations"),
    "governance": ("governance_objects", "Related Governance Objects"),
    "governance_object": ("governance_objects", "Related Governance Objects"),
    "control": ("governance_objects", "Related Governance Objects"),
}

_DEFAULT_RELATED_OBJECTS = (
    ("processes", "Related Processes"),
    ("risks", "Related Risks"),
    ("policies", "Related Policies"),
    ("scenarios", "Related Scenarios"),
    ("observations", "Related Observations"),
    ("governance_objects", "Related Governance Objects"),
)
=======
from typing import Any
from uuid import uuid4

from sqlalchemy.orm.attributes import flag_modified

from app.domains.context.context_relationship_config import get_relationship_type


def _metadata(context_object) -> dict[str, Any]:
    metadata = getattr(context_object, "metadata_json", None)
    if not isinstance(metadata, dict):
        metadata = {}
    context_object.metadata_json = metadata
    return metadata
>>>>>>> Stashed changes


def _object_label(context_type: str) -> tuple[str, str] | None:
    return _RELATED_OBJECT_CATEGORIES.get((context_type or "").strip().lower())


<<<<<<< Updated upstream
=======
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


def detect_context_conflicts(relationships) -> list[dict[str, Any]]:
    return []

_RELATED_OBJECT_CATEGORIES = {
    "process": ("processes", "Related Processes"),
    "risk": ("risks", "Related Risks"),
    "policy": ("policies", "Related Policies"),
    "scenario": ("scenarios", "Related Scenarios"),
    "observation": ("observations", "Related Observations"),
    "governance": ("governance_objects", "Related Governance Objects"),
    "governance_object": ("governance_objects", "Related Governance Objects"),
    "control": ("governance_objects", "Related Governance Objects"),
}

_DEFAULT_RELATED_OBJECTS = (
    ("processes", "Related Processes"),
    ("risks", "Related Risks"),
    ("policies", "Related Policies"),
    ("scenarios", "Related Scenarios"),
    ("observations", "Related Observations"),
    ("governance_objects", "Related Governance Objects"),
)


def _object_label(context_type: str) -> tuple[str, str] | None:
    return _RELATED_OBJECT_CATEGORIES.get((context_type or "").strip().lower())


>>>>>>> Stashed changes
def _awareness_item(context_object, relationship: dict[str, Any] | None = None) -> dict[str, Any]:
    metadata = getattr(context_object, "metadata_json", None) or {}
    item = {
        "id": str(getattr(context_object, "id", "")),
        "name": getattr(context_object, "name", None) or metadata.get("name") or str(getattr(context_object, "id", "")),
        "description": getattr(context_object, "description", None),
        "context_type": getattr(context_object, "context_type", None),
        "owner": getattr(context_object, "owner", None),
        "confidence": getattr(context_object, "confidence", None),
        "source": getattr(context_object, "source", None),
        "relationship_type": relationship.get("type") if relationship else None,
        "relationship_label": relationship.get("label") if relationship else None,
        "reason": relationship.get("reason") if relationship else None,
        "url": None,
    }
    return item


def _empty_related_objects() -> dict[str, dict[str, Any]]:
    return {
        key: {"label": label, "count": 0, "items": []}
        for key, label in _DEFAULT_RELATED_OBJECTS
    }


def build_decision_relationship_awareness(decision) -> dict[str, Any]:
    """Build a user-facing relationship awareness view for a decision.

    The structure intentionally uses product language such as related objects and
    impact instead of technical graph terminology.
    """
    context_objects = list(getattr(decision, "context_objects", []) or [])
    objects_by_id = {str(obj.id): obj for obj in context_objects}
    related_objects = _empty_related_objects()
    seen_by_category: dict[str, set[str]] = {key: set() for key in related_objects}
    influenced_by: list[dict[str, Any]] = []
    influences: list[dict[str, Any]] = []
    seen_influenced_by: set[str] = set()
    seen_influences: set[str] = set()

    def add_related(obj, relationship: dict[str, Any] | None = None):
        mapping = _object_label(getattr(obj, "context_type", None))
        if mapping is None:
            return
        key, _label = mapping
        object_id = str(getattr(obj, "id", ""))
        if not object_id or object_id in seen_by_category[key]:
            return
        related_objects[key]["items"].append(_awareness_item(obj, relationship))
        seen_by_category[key].add(object_id)
        related_objects[key]["count"] = len(related_objects[key]["items"])

    def add_impact(target_list: list[dict[str, Any]], seen: set[str], obj, relationship: dict[str, Any] | None = None):
        object_id = str(getattr(obj, "id", ""))
        if not object_id or object_id in seen:
            return
        target_list.append(_awareness_item(obj, relationship))
        seen.add(object_id)

    for obj in context_objects:
        add_related(obj)
        add_impact(influenced_by, seen_influenced_by, obj)

    for source in context_objects:
        for relationship in list_context_relationships(source):
            target = objects_by_id.get(str(relationship.get("target_context_id")))
            if target is None:
                continue
            add_related(target, relationship)
            add_impact(influences, seen_influences, target, relationship)
<<<<<<< Updated upstream
=======

    summary_counts = {
        key: value.get("count", 0)
        for key, value in related_objects.items()
    }
>>>>>>> Stashed changes

    return {
        "related_objects": related_objects,
        "summary_counts": summary_counts,
        "impact": {
            "influenced_by": influenced_by,
            "influences": influences,
        },
    }


def build_context_related_objects(context_object, decision=None) -> dict[str, Any]:
    objects = list(getattr(decision, "context_objects", []) or []) if decision is not None else []
    objects_by_id = {str(obj.id): obj for obj in objects}
    related = []
    seen: set[str] = set()
    for relationship in list_context_relationships(context_object):
        target = objects_by_id.get(str(relationship.get("target_context_id")))
        if target is None:
            continue
        target_id = str(target.id)
        if target_id in seen:
            continue
        related.append(_awareness_item(target, relationship))
        seen.add(target_id)
    return {"context_id": str(context_object.id), "related_objects": related, "count": len(related)}
