from __future__ import annotations

from datetime import datetime
from typing import Any

from app.domains.context.models import DecisionContextObject
from app.domains.context.risk_config import ContextTaxonomy, get_risk_taxonomy
from app.domains.context.types import CONFIDENCE_VALUES, CONTEXT_TYPES
from app.domains.decision.models import Decision
from app.domains.scenario.models import Scenario
from app.shared.errors import NotFoundError


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
