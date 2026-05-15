from flask import Blueprint, jsonify, request

from app.domains.assessment.service import RiskAssessmentService
from app.domains.governance.schemas import (
    ApprovalCreateSchema,
    DecisionRecordResponseSchema,
    RiskAssessmentCreateSchema,
    SimpleGovernanceResponseSchema,
)
from app.domains.governance.service import GovernanceService
from app.shared.database import session_scope
from app.shared.schemas import load_json
from app.shared.request_context import actor_from_request

bp = Blueprint("governance", __name__)


def payload():
    return request.get_json(silent=True) or {}


@bp.post("/decisions/<decision_id>/risks")
def create_risk(decision_id):
    data = load_json(RiskAssessmentCreateSchema(), payload())
    with session_scope() as session:
        risk = RiskAssessmentService(session).create_risk_assessment(
            decision_id=decision_id,
            summary=data["summary"],
            severity=data.get("severity", "medium"),
            mitigation=data.get("mitigation"),
            created_by=actor_from_request(data),
        )
        return jsonify(SimpleGovernanceResponseSchema().dump(risk)), 201


@bp.post("/decisions/<decision_id>/approvals")
def create_approval(decision_id):
    data = load_json(ApprovalCreateSchema(), payload())
    with session_scope() as session:
        approval = GovernanceService(session).create_approval_record(
            decision_id=decision_id,
            approved_by=data["approved_by"],
            status=data.get("status", "approved"),
            comment=data.get("comment"),
            created_by=actor_from_request(data),
        )
        return jsonify(SimpleGovernanceResponseSchema().dump(approval)), 201


@bp.post("/decisions/<decision_id>/records")
def create_record(decision_id):
    with session_scope() as session:
        record = GovernanceService(session).create_decision_record(decision_id, created_by=actor_from_request(payload()))
        return jsonify(DecisionRecordResponseSchema().dump(record)), 201
