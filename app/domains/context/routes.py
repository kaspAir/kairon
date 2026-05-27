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
from app.domains.context.process_config import get_process_taxonomy
from app.domains.context.risk_config import get_risk_taxonomy
from app.domains.context.service import DecisionContextService
from app.shared.database import session_scope
from app.shared.schemas import load_json

bp = Blueprint("context", __name__)


def payload():
    return request.get_json(silent=True) or {}


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
