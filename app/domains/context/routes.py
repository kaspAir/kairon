from flask import Blueprint, jsonify, request

from app.domains.context.schemas import (
    DecisionContextObjectCreateSchema,
    DecisionContextObjectResponseSchema,
    DecisionContextObjectUpdateSchema,
    ProcessContextCreateSchema,
    ProcessContextResponseSchema,
    RiskContextCreateSchema,
    RiskContextResponseSchema,
)
from app.domains.context.context_relationship_config import list_active_relationship_types
from app.domains.context.process_config import get_process_taxonomy
from app.domains.context.risk_config import get_risk_taxonomy
from app.domains.context.service import DecisionContextService
from app.shared.database import session_scope
from app.shared.schemas import load_json

from app.domains.context.link_config import context_link_config_view_model

bp = Blueprint("context", __name__)


def payload():
    return request.get_json(silent=True) or {}




@bp.get("/context/relationships/types")
def list_context_relationship_types():
    return jsonify({
        "relationship_types": [
            relationship_type.as_dict()
            for relationship_type in list_active_relationship_types()
        ]
    })


@bp.post("/context/<context_object_id>/relationships")
def create_context_relationship(context_object_id):
    data = payload()
    relationship_type = data.get("type")
    target_context_id = data.get("target_context_id")

    if not relationship_type:
        return jsonify({"error": {"code": "validation_error", "message": "type is required", "status": 400}}), 400
    if not target_context_id:
        return jsonify({"error": {"code": "validation_error", "message": "target_context_id is required", "status": 400}}), 400

    with session_scope() as session:
        relationship = DecisionContextService(session).add_context_relationship(
            context_object_id,
            relationship_type=relationship_type,
            target_context_id=target_context_id,
            target_context_type=data.get("target_context_type"),
            label=data.get("label"),
            reason=data.get("reason"),
            confidence=data.get("confidence"),
            extra=data.get("extra"),
        )
        return jsonify({"relationship": relationship}), 201


@bp.get("/decisions/<decision_id>/context-relationships")
def decision_context_relationships(decision_id):
    with session_scope() as session:
        service = DecisionContextService(session)
        return jsonify({
            "decision_id": decision_id,
            "summary": service.summarize_context_relationships(decision_id),
        })




@bp.get("/decisions/<decision_id>/relationship-awareness")
def decision_relationship_awareness(decision_id):
    with session_scope() as session:
        service = DecisionContextService(session)
        return jsonify({
            "decision_id": decision_id,
            "relationship_awareness": service.relationship_awareness_for_decision(decision_id),
        })


@bp.get("/context/<context_object_id>/related-objects")
def context_related_objects(context_object_id):
    with session_scope() as session:
        service = DecisionContextService(session)
        return jsonify(service.related_objects_for_context(context_object_id))


@bp.get("/decisions/<decision_id>/context-objects")
def list_context_objects(decision_id):
    with session_scope() as session:
        objects = DecisionContextService(session).list_context_objects(decision_id)
        return jsonify(DecisionContextObjectResponseSchema(many=True).dump(objects))


@bp.post("/decisions/<decision_id>/context-objects")
def create_context_object(decision_id):
    data = load_json(DecisionContextObjectCreateSchema(), payload())
    with session_scope() as session:
        context_object = DecisionContextService(session).create_context_object(decision_id=decision_id, **data)
        return jsonify(DecisionContextObjectResponseSchema().dump(context_object)), 201


@bp.get("/decisions/<decision_id>/process-contexts")
def list_process_contexts(decision_id):
    with session_scope() as session:
        service = DecisionContextService(session)
        contexts = service.list_process_contexts_for_decision(decision_id)
        return jsonify({
            "items": ProcessContextResponseSchema(many=True).dump(contexts),
            "taxonomy": get_process_taxonomy().as_dict(),
        })


@bp.post("/decisions/<decision_id>/process-contexts")
def create_process_context(decision_id):
    data = load_json(ProcessContextCreateSchema(), payload())
    with session_scope() as session:
        process_context = DecisionContextService(session).create_process_context(
            decision_id=decision_id,
            **data,
        )
        return jsonify(ProcessContextResponseSchema().dump(process_context)), 201


@bp.get("/decisions/<decision_id>/risks")
def list_risk_contexts(decision_id):
    with session_scope() as session:
        service = DecisionContextService(session)
        risks = service.list_risks_for_decision(decision_id)
        taxonomy = get_risk_taxonomy().as_dict()
        return jsonify({
            "items": RiskContextResponseSchema(many=True).dump(risks),
            "summary": service.summarize_risks_for_decision(decision_id),
            "taxonomy": taxonomy,
        })


@bp.post("/decisions/<decision_id>/risks")
def create_risk_context(decision_id):
    data = load_json(RiskContextCreateSchema(), payload())
    with session_scope() as session:
        risk = DecisionContextService(session).create_risk_context(decision_id=decision_id, **data)
        return jsonify(RiskContextResponseSchema().dump(risk)), 201


@bp.patch("/context-objects/<context_object_id>")
def update_context_object(context_object_id):
    data = load_json(DecisionContextObjectUpdateSchema(), payload())
    with session_scope() as session:
        context_object = DecisionContextService(session).update_context_object(context_object_id, **data)
        return jsonify(DecisionContextObjectResponseSchema().dump(context_object))


@bp.delete("/context-objects/<context_object_id>")
def delete_context_object(context_object_id):
    with session_scope() as session:
        DecisionContextService(session).delete_context_object(context_object_id)
        return "", 204
    
@bp.get("/process-landscape")
def process_landscape():
    with session_scope() as session:
        service = DecisionContextService(session)
        items = service.process_landscape_items()
        grouped: dict[str, list[dict]] = {}
        for item in items:
            grouped.setdefault(item.get("process_level") or "unknown", []).append(item)
        return jsonify({
            "items": items,
            "grouped": grouped,
            "context_link_config": context_link_config_view_model(),
        })

