from flask import Blueprint, jsonify, request

from app.domains.decision.models import Decision
from app.domains.decision.schemas import (
    DecisionCreateSchema,
    DecisionResponseSchema,
    DecisionVariantCreateSchema,
    DecisionVariantResponseSchema,
    DecisionStatusTransitionSchema,
)
from app.domains.decision.service import DecisionService
from app.domains.decision.status import allowed_next_statuses
from app.shared.database import session_scope
from app.shared.schemas import load_json
from app.shared.request_context import actor_from_request

bp = Blueprint("decision", __name__)


def payload():
    return request.get_json(silent=True) or {}


@bp.get("/decisions")
def list_decisions():
    with session_scope() as session:
        decisions = session.query(Decision).order_by(Decision.created_at.desc()).all()
        return jsonify(DecisionResponseSchema(many=True).dump(decisions))


@bp.post("/decisions")
def create_decision():
    data = load_json(DecisionCreateSchema(), payload())
    description = data.get("description") or data.get("context")
    with session_scope() as session:
        decision = DecisionService(session).create_decision(data["title"], description, created_by=actor_from_request(data))
        return jsonify(DecisionResponseSchema().dump(decision)), 201


@bp.post("/decisions/<decision_id>/variants")
def create_variant(decision_id):
    data = load_json(DecisionVariantCreateSchema(), payload())
    with session_scope() as session:
        variant = DecisionService(session).create_variant(
            decision_id=decision_id,
            name=data["name"],
            description=data.get("description"),
            estimated_cost=data.get("estimated_cost", 0),
            expected_benefit=data.get("expected_benefit", 0),
            created_by=actor_from_request(data),
        )
        return jsonify(DecisionVariantResponseSchema().dump(variant)), 201


@bp.post("/decisions/<decision_id>/status")
def change_decision_status(decision_id):
    data = load_json(DecisionStatusTransitionSchema(), payload())
    with session_scope() as session:
        service = DecisionService(session)
        decision, previous_status = service.change_decision_status(
            decision_id=decision_id,
            target_status=data["status"],
            changed_by=actor_from_request(data),
        )
        return jsonify({
            "id": decision.id,
            "title": decision.title,
            "status": decision.status,
            "previous_status": previous_status,
            "allowed_next_statuses": list(allowed_next_statuses(decision.status)),
            "updated_at": decision.updated_at.isoformat(),
            "version": decision.version,
            "audit_notice": "Status transition validated by DecisionService; Decision Record integration prepared.",
        })


@bp.get("/decisions/<decision_id>/record")
def show_decision_record(decision_id):
    with session_scope() as session:
        view = DecisionService(session).get_decision_record_view(decision_id)
        return jsonify(view)
