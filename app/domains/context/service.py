from __future__ import annotations

from datetime import datetime
from typing import Any

from app.domains.context.models import DecisionContextObject
from app.domains.context.context_relationship_service import (
    add_context_relationship as add_relationship_to_context_object,
    build_context_related_objects,
    build_decision_relationship_awareness,
    count_context_relationships,
    list_context_relationships,
    summarize_context_relationships,
)
from app.domains.context.process_config import ProcessTaxonomy, get_process_taxonomy
from app.domains.context.risk_config import ContextTaxonomy, get_risk_taxonomy
from app.domains.context.types import CONFIDENCE_VALUES, CONTEXT_TYPES
from app.domains.decision.models import Decision
from app.domains.scenario.models import Scenario
from app.shared.errors import NotFoundError

from app.domains.context.process_config import ProcessTaxonomy, get_process_taxonomy


class DecisionContextService:
    def __init__(self, session):
        self.session = session

    def list_context_objects(self, decision_id: str) -> list[DecisionContextObject]:
        self._require_decision(decision_id)
        return (
            self.session.query(DecisionContextObject)
            .filter(DecisionContextObject.decision_id == decision_id)
            .order_by(DecisionContextObject.context_type.asc(), DecisionContextObject.created_at.desc())
            .all()
        )

    def create_context_object(
        self,
        *,
        decision_id: str,
        context_type: str,
        name: str,
        scenario_id: str | None = None,
        description: str | None = None,
        source: str | None = None,
        owner: str | None = None,
        confidence: str = "medium",
        valid_from: datetime | None = None,
        valid_to: datetime | None = None,
        metadata_json: dict[str, Any] | None = None,
    ) -> DecisionContextObject:
        self._require_decision(decision_id)
        if scenario_id:
            scenario = self.session.get(Scenario, scenario_id)
            if scenario is None or scenario.decision_id != decision_id:
                raise NotFoundError("Scenario not found for decision")
        context_type = self._validate_context_type(context_type)
        confidence = self._validate_confidence(confidence)
        name = (name or "").strip()
        if not name:
            raise ValueError("Context object name is required")
        if valid_from and valid_to and valid_to < valid_from:
            raise ValueError("valid_to must be after valid_from")

        context_object = DecisionContextObject(
            decision_id=decision_id,
            scenario_id=scenario_id or None,
            context_type=context_type,
            name=name,
            description=description,
            source=source,
            owner=owner,
            confidence=confidence,
            valid_from=valid_from,
            valid_to=valid_to,
            metadata_json=metadata_json or {},
        )
        self.session.add(context_object)
        self.session.flush()
        return context_object


    def create_process_context(
        self,
        *,
        decision_id: str,
        name: str,
        description: str | None = None,
        process_level: str | None = None,
        owner: str | None = None,
        scope: str | None = None,
        source: str | None = None,
        confidence: str = "medium",
        scenario_id: str | None = None,
        created_by: str = "system",
        taxonomy: ProcessTaxonomy | None = None,
    ) -> DecisionContextObject:
        taxonomy = taxonomy or get_process_taxonomy()
        process_name = (name or "").strip()
        if not process_name:
            raise ValueError("Process context name is required")
        level = self._validate_taxonomy_value(
            "process_level",
            process_level or taxonomy.levels[3],
            taxonomy.levels,
        )
        metadata = {
            "process_level": level,
            "process_level_label": taxonomy.label_for(level),
            "scope": scope,
            "created_by": created_by or "system",
        }
        return self.create_context_object(
            decision_id=decision_id,
            scenario_id=scenario_id,
            context_type="process",
            name=process_name,
            description=description,
            source=source,
            owner=owner,
            confidence=confidence,
            metadata_json=metadata,
        )

    def list_process_contexts_for_decision(self, decision_id: str) -> list[DecisionContextObject]:
        self._require_decision(decision_id)
        return (
            self.session.query(DecisionContextObject)
            .filter(DecisionContextObject.decision_id == decision_id)
            .filter(DecisionContextObject.context_type == "process")
            .order_by(DecisionContextObject.created_at.desc())
            .all()
        )


    def create_risk_context(
        self,
        *,
        decision_id: str,
        name: str | None = None,
        summary: str | None = None,
        description: str | None = None,
        category: str | None = None,
        probability: str | None = None,
        impact: str | None = None,
        severity: str | None = None,
        impact_area: str | None = None,
        mitigation: str | None = None,
        risk_owner: str | None = None,
        review_required: bool = False,
        source: str | None = None,
        owner: str | None = None,
        confidence: str = "medium",
        scenario_id: str | None = None,
        created_by: str = "system",
        taxonomy: ContextTaxonomy | None = None,
    ) -> DecisionContextObject:
        taxonomy = taxonomy or get_risk_taxonomy()
        risk_name = (name or summary or "").strip()
        if not risk_name:
            raise ValueError("Risk name is required")

        metadata = {
            "category": (category or "implementation").strip(),
            "probability": self._validate_taxonomy_value("probability", probability or taxonomy.probability_values[1], taxonomy.probability_values),
            "impact": self._validate_taxonomy_value("impact", impact or taxonomy.impact_values[1], taxonomy.impact_values),
            "severity": self._validate_taxonomy_value("severity", severity or taxonomy.severity_values[1], taxonomy.severity_values),
            "impact_area": self._validate_taxonomy_value("impact_area", impact_area or taxonomy.impact_area_values[0], taxonomy.impact_area_values),
            "mitigation": mitigation,
            "risk_owner": risk_owner or owner,
            "review_required": bool(review_required),
            "created_by": created_by or "system",
        }

        return self.create_context_object(
            decision_id=decision_id,
            scenario_id=scenario_id,
            context_type="risk",
            name=risk_name,
            description=description or summary,
            source=source,
            owner=owner or risk_owner,
            confidence=confidence,
            metadata_json=metadata,
        )

    def list_risks_for_decision(self, decision_id: str) -> list[DecisionContextObject]:
        self._require_decision(decision_id)
        return (
            self.session.query(DecisionContextObject)
            .filter(DecisionContextObject.decision_id == decision_id)
            .filter(DecisionContextObject.context_type == "risk")
            .order_by(DecisionContextObject.created_at.desc())
            .all()
        )

    def summarize_risks_for_decision(self, decision_id: str) -> dict[str, object]:
        risks = self.list_risks_for_decision(decision_id)
        by_severity: dict[str, int] = {}
        review_required = 0
        for risk in risks:
            metadata = risk.metadata_json or {}
            severity = metadata.get("severity", "unknown")
            by_severity[severity] = by_severity.get(severity, 0) + 1
            if metadata.get("review_required"):
                review_required += 1
        return {
            "total": len(risks),
            "critical": by_severity.get("critical", 0),
            "by_severity": by_severity,
            "review_required": review_required,
        }


    def add_context_relationship(
        self,
        context_object_id: str,
        *,
        relationship_type: str,
        target_context_id: str,
        target_context_type: str | None = None,
        label: str | None = None,
        reason: str | None = None,
        confidence: str | None = None,
        extra: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        context_object = self._require_context_object(context_object_id)
        relationship = add_relationship_to_context_object(
            context_object,
            relationship_type=relationship_type,
            target_context_id=target_context_id,
            target_context_type=target_context_type,
            label=label,
            reason=reason,
            confidence=confidence,
            extra=extra,
        )
        self.session.add(context_object)
        self.session.flush()
        return relationship

    def list_context_relationships(self, context_object_id: str) -> list[dict[str, Any]]:
        context_object = self._require_context_object(context_object_id)
        return list_context_relationships(context_object)

    def count_context_relationships(self, context_object_id: str) -> int:
        context_object = self._require_context_object(context_object_id)
        return count_context_relationships(context_object)

    def summarize_context_relationships(self, decision_id: str) -> list[dict[str, Any]]:
        context_objects = self.list_context_objects(decision_id)
        return summarize_context_relationships(context_objects)

    def relationship_awareness_for_decision(self, decision_id: str) -> dict[str, Any]:
        decision = self._require_decision(decision_id)
        context_objects = self.list_context_objects(decision_id)
        return build_decision_relationship_awareness(decision, context_objects=context_objects)

    def related_objects_for_context(self, context_object_id: str) -> dict[str, Any]:
        context_object = self._require_context_object(context_object_id)
        context_objects = self.list_context_objects(context_object.decision_id)
        return build_context_related_objects(context_object, all_context_objects=context_objects)

    def update_context_object(self, context_object_id: str, **changes) -> DecisionContextObject:
        context_object = self._require_context_object(context_object_id)
        if "context_type" in changes and changes["context_type"] is not None:
            context_object.context_type = self._validate_context_type(changes["context_type"])
        if "confidence" in changes and changes["confidence"] is not None:
            context_object.confidence = self._validate_confidence(changes["confidence"])
        for field in ("name", "description", "source", "owner", "scenario_id", "valid_from", "valid_to", "metadata_json"):
            if field in changes:
                setattr(context_object, field, changes[field])
        if not (context_object.name or "").strip():
            raise ValueError("Context object name is required")
        if context_object.valid_from and context_object.valid_to and context_object.valid_to < context_object.valid_from:
            raise ValueError("valid_to must be after valid_from")
        self.session.flush()
        return context_object

    def delete_context_object(self, context_object_id: str) -> None:
        context_object = self._require_context_object(context_object_id)
        self.session.delete(context_object)
        self.session.flush()

    def _require_decision(self, decision_id: str) -> Decision:
        decision = self.session.get(Decision, decision_id)
        if decision is None:
            raise NotFoundError("Decision not found")
        return decision

    def _require_context_object(self, context_object_id: str) -> DecisionContextObject:
        context_object = self.session.get(DecisionContextObject, context_object_id)
        if context_object is None:
            raise NotFoundError("Context object not found")
        return context_object

    def _validate_taxonomy_value(self, field: str, value: str, allowed_values: tuple[str, ...]) -> str:
        normalized = (value or "").strip().lower()
        if normalized not in allowed_values:
            raise ValueError(f"Invalid {field}: {normalized}")
        return normalized

    def _validate_context_type(self, context_type: str) -> str:
        value = (context_type or "").strip().lower()
        if value not in CONTEXT_TYPES:
            raise ValueError("Invalid context type")
        return value

    def _validate_confidence(self, confidence: str) -> str:
        value = (confidence or "medium").strip().lower()
        if value not in CONFIDENCE_VALUES:
            raise ValueError("Invalid confidence")
        return value
    
    def list_process_contexts(
        self,
        decision_id: str | None = None,
    ) -> list[DecisionContextObject]:
        query = (
            self.session.query(DecisionContextObject)
            .filter(DecisionContextObject.context_type == "process")
            .order_by(DecisionContextObject.created_at.desc())
        )
        if decision_id:
            self._require_decision(decision_id)
            query = query.filter(DecisionContextObject.decision_id == decision_id)
        return query.all()

    def process_landscape_items(self) -> list[dict[str, Any]]:
        process_contexts = self.list_process_contexts()
        items = []
        for obj in process_contexts:
            metadata = obj.metadata_json or {}
            decision = getattr(obj, "decision", None)
            related_context_count = 0
            if decision is not None:
                related_context_count = max(len(getattr(decision, "context_objects", [])) - 1, 0)
            items.append({
                "id": obj.id,
                "decision_id": obj.decision_id,
                "decision_title": decision.title if decision is not None else None,
                "name": obj.name,
                "description": obj.description,
                "owner": obj.owner,
                "scope": metadata.get("scope"),
                "source": obj.source,
                "confidence": obj.confidence,
                "process_level": metadata.get("process_level"),
                "process_level_label": metadata.get("process_level_label") or (metadata.get("process_level") or "").replace("_", " ").title(),
                "related_context_count": related_context_count,
                "relationship_count": count_context_relationships(obj),
                "created_at": obj.created_at,
            })
        return items
