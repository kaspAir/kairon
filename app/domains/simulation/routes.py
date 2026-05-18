from flask import Blueprint, jsonify, request

from app.domains.simulation.schemas import SimulationRunResponseSchema
from app.domains.simulation.service import SimulationService
from app.shared.database import session_scope
from app.shared.request_context import actor_from_request

bp = Blueprint("simulation", __name__)


@bp.post("/scenarios/<scenario_id>/simulate")
def simulate(scenario_id):
    with session_scope() as session:
        run = SimulationService(session).run_deterministic_simulation(scenario_id, created_by=actor_from_request(request.get_json(silent=True) or {}))
        return jsonify(SimulationRunResponseSchema().dump(run)), 201
