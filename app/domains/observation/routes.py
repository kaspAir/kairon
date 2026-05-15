from flask import Blueprint, jsonify, request

from app.domains.observation.schemas import ObservationCreateSchema, ObservationResponseSchema
from app.domains.observation.service import ObservationService
from app.shared.database import session_scope
from app.shared.request_context import actor_from_request
from app.shared.schemas import load_json

bp = Blueprint("observation", __name__)


def payload():
    return request.get_json(silent=True) or {}


@bp.post("/decisions/<decision_id>/observations")
def create_observation(decision_id):
    data = load_json(ObservationCreateSchema(), payload())
    with session_scope() as session:
        observation = ObservationService(session).create_observation_record(
            decision_id=decision_id,
            expected_benefit=data["expected_benefit"],
            actual_benefit=data["actual_benefit"],
            expected_cost=data["expected_cost"],
            actual_cost=data["actual_cost"],
            expected_risks=data.get("expected_risks"),
            actual_risks=data.get("actual_risks"),
            comment=data.get("comment"),
            observed_at=data.get("observed_at"),
            created_by=actor_from_request(data),
        )
        return jsonify(ObservationResponseSchema().dump(observation)), 201
