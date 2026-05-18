from marshmallow import Schema, fields, validate

from app.domains.context.types import CONFIDENCE_VALUES, CONTEXT_TYPES
from app.shared.schemas import non_empty


class DecisionContextObjectCreateSchema(Schema):
    scenario_id = fields.String(load_default=None, allow_none=True)
    context_type = fields.String(required=True, validate=validate.OneOf(CONTEXT_TYPES))
    name = fields.String(required=True, validate=non_empty)
    description = fields.String(load_default=None, allow_none=True)
    source = fields.String(load_default=None, allow_none=True)
    owner = fields.String(load_default=None, allow_none=True)
    confidence = fields.String(load_default="medium", validate=validate.OneOf(CONFIDENCE_VALUES))
    valid_from = fields.DateTime(load_default=None, allow_none=True)
    valid_to = fields.DateTime(load_default=None, allow_none=True)
    metadata_json = fields.Dict(load_default=dict)


class DecisionContextObjectUpdateSchema(Schema):
    scenario_id = fields.String(load_default=None, allow_none=True)
    context_type = fields.String(validate=validate.OneOf(CONTEXT_TYPES))
    name = fields.String(validate=non_empty)
    description = fields.String(allow_none=True)
    source = fields.String(allow_none=True)
    owner = fields.String(allow_none=True)
    confidence = fields.String(validate=validate.OneOf(CONFIDENCE_VALUES))
    valid_from = fields.DateTime(allow_none=True)
    valid_to = fields.DateTime(allow_none=True)
    metadata_json = fields.Dict()


class DecisionContextObjectResponseSchema(Schema):
    id = fields.String(required=True)
    decision_id = fields.String(required=True)
    scenario_id = fields.String(allow_none=True)
    context_type = fields.String(required=True)
    name = fields.String(required=True)
    description = fields.String(allow_none=True)
    source = fields.String(allow_none=True)
    owner = fields.String(allow_none=True)
    confidence = fields.String(required=True)
    valid_from = fields.DateTime(allow_none=True)
    valid_to = fields.DateTime(allow_none=True)
    metadata_json = fields.Dict(allow_none=True)
    created_at = fields.DateTime(required=True)
    updated_at = fields.DateTime(required=True)
