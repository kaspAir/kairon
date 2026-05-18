from marshmallow import Schema, fields, validate

from app.shared.schemas import non_empty


class DecisionCreateSchema(Schema):
    title = fields.String(required=True, validate=non_empty)
    description = fields.String(load_default=None, allow_none=True)
    context = fields.String(load_default=None, allow_none=True)
    created_by = fields.String(load_default="system")


class DecisionResponseSchema(Schema):
    id = fields.String(required=True)
    title = fields.String(required=True)
    description = fields.String(attribute="context", allow_none=True)
    status = fields.String(required=True)
    created_at = fields.DateTime(required=True)
    updated_at = fields.DateTime(required=True)
    version = fields.Integer(required=True)
    created_by = fields.String(required=True)


class DecisionVariantCreateSchema(Schema):
    name = fields.String(required=True, validate=non_empty)
    description = fields.String(load_default=None, allow_none=True)
    estimated_cost = fields.Float(load_default=0, validate=validate.Range(min=0))
    expected_benefit = fields.Float(load_default=0, validate=validate.Range(min=0))
    created_by = fields.String(load_default="system")


class DecisionVariantResponseSchema(Schema):
    id = fields.String(required=True)
    decision_id = fields.String(required=True)
    name = fields.String(required=True)
    description = fields.String(allow_none=True)
    estimated_cost = fields.Float(required=True)
    expected_benefit = fields.Float(required=True)
    status = fields.String(required=True)
    created_at = fields.DateTime(required=True)
    updated_at = fields.DateTime(required=True)
    version = fields.Integer(required=True)
    created_by = fields.String(required=True)



class DecisionStatusTransitionSchema(Schema):
    status = fields.String(required=True, validate=non_empty)
    created_by = fields.String(load_default="system")


class DecisionStatusTransitionResponseSchema(Schema):
    id = fields.String(required=True)
    title = fields.String(required=True)
    status = fields.String(required=True)
    previous_status = fields.String(required=True)
    allowed_next_statuses = fields.List(fields.String(), required=True)
    updated_at = fields.DateTime(required=True)
    version = fields.Integer(required=True)
