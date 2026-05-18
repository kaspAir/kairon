from marshmallow import Schema, fields, validate

from app.shared.schemas import non_empty


class ScenarioCreateSchema(Schema):
    variant_id = fields.String(required=True, validate=non_empty)
    name = fields.String(required=True, validate=non_empty)
    description = fields.String(load_default=None, allow_none=True)
    case_volume = fields.Integer(load_default=1, validate=validate.Range(min=0))
    processing_minutes_per_case = fields.Float(load_default=0, validate=validate.Range(min=0))
    hourly_cost = fields.Float(load_default=0, validate=validate.Range(min=0))
    created_by = fields.String(load_default="system")


class ScenarioResponseSchema(Schema):
    id = fields.String(required=True)
    decision_id = fields.String(required=True)
    variant_id = fields.String(required=True)
    name = fields.String(required=True)
    description = fields.String(allow_none=True)
    case_volume = fields.Integer(required=True)
    processing_minutes_per_case = fields.Float(required=True)
    hourly_cost = fields.Float(required=True)
    status = fields.String(required=True)
    created_at = fields.DateTime(required=True)
    updated_at = fields.DateTime(required=True)
    version = fields.Integer(required=True)
    created_by = fields.String(required=True)
