from marshmallow import Schema, fields, validate

from app.shared.schemas import non_empty


class RiskAssessmentCreateSchema(Schema):
    summary = fields.String(required=True, validate=non_empty)
    severity = fields.String(load_default="medium", validate=validate.OneOf(["low", "medium", "high"]))
    mitigation = fields.String(load_default=None, allow_none=True)
    created_by = fields.String(load_default="system")


class ApprovalCreateSchema(Schema):
    approved_by = fields.String(required=True, validate=non_empty)
    status = fields.String(load_default="approved", validate=validate.OneOf(["approved", "rejected", "needs_review"]))
    comment = fields.String(load_default=None, allow_none=True)
    created_by = fields.String(load_default="system")


class SimpleGovernanceResponseSchema(Schema):
    id = fields.String(required=True)
    decision_id = fields.String(required=True)
    status = fields.String(required=True)
    created_at = fields.DateTime(required=True)
    updated_at = fields.DateTime(required=True)
    version = fields.Integer(required=True)
    created_by = fields.String(required=True)


class DecisionRecordResponseSchema(SimpleGovernanceResponseSchema):
    record_text = fields.String(required=True)
