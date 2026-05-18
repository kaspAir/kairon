from flask import Blueprint, jsonify, request

from app.domains.context.schemas import (
    DecisionContextObjectCreateSchema,
    DecisionContextObjectResponseSchema,
    DecisionContextObjectUpdateSchema,
)
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
