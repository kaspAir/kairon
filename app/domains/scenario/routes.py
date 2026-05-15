from flask import Blueprint, jsonify, request

from app.domains.scenario.schemas import ScenarioCreateSchema, ScenarioResponseSchema
from app.domains.scenario.service import ScenarioService
from app.shared.database import session_scope
from app.shared.schemas import load_json
from app.shared.request_context import actor_from_request

bp = Blueprint("scenario", __name__)


def payload():
    return request.get_json(silent=True) or {}


@bp.post("/decisions/<decision_id>/scenarios")
def create_scenario(decision_id):
    data = load_json(ScenarioCreateSchema(), payload())
    with session_scope() as session:
        scenario = ScenarioService(session).create_scenario(
            decision_id=decision_id,
            variant_id=data["variant_id"],
            name=data["name"],
            description=data.get("description"),
            case_volume=data.get("case_volume", 1),
            processing_minutes_per_case=data.get("processing_minutes_per_case", 0),
            hourly_cost=data.get("hourly_cost", 0),
            created_by=actor_from_request(data),
        )
        return jsonify(ScenarioResponseSchema().dump(scenario)), 201
