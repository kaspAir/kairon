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


class RiskContextCreateSchema(Schema):
    # `summary` is accepted for backwards compatibility with the earlier MVP API.
    name = fields.String(load_default=None, allow_none=True)
    summary = fields.String(load_default=None, allow_none=True)
    description = fields.String(load_default=None, allow_none=True)
    category = fields.String(load_default="implementation")
    probability = fields.String(load_default=None, allow_none=True)
    impact = fields.String(load_default=None, allow_none=True)
    severity = fields.String(load_default=None, allow_none=True)
    impact_area = fields.String(load_default=None, allow_none=True)
    mitigation = fields.String(load_default=None, allow_none=True)
    risk_owner = fields.String(load_default=None, allow_none=True)
    review_required = fields.Boolean(load_default=False)
    source = fields.String(load_default=None, allow_none=True)
    owner = fields.String(load_default=None, allow_none=True)
    confidence = fields.String(load_default="medium", validate=validate.OneOf(CONFIDENCE_VALUES))
    scenario_id = fields.String(load_default=None, allow_none=True)
    created_by = fields.String(load_default="system")


class RiskContextResponseSchema(Schema):
    id = fields.String(required=True)
    decision_id = fields.String(required=True)
    scenario_id = fields.String(allow_none=True)
    context_type = fields.String(required=True)
    name = fields.String(required=True)
    summary = fields.Method("get_summary")
    description = fields.String(allow_none=True)
    source = fields.String(allow_none=True)
    owner = fields.String(allow_none=True)
    confidence = fields.String(required=True)
    probability = fields.Method("get_probability")
    impact = fields.Method("get_impact")
    severity = fields.Method("get_severity")
    impact_area = fields.Method("get_impact_area")
    mitigation = fields.Method("get_mitigation")
    created_by = fields.Method("get_created_by")
    metadata_json = fields.Dict(allow_none=True)
    created_at = fields.DateTime(required=True)
    updated_at = fields.DateTime(required=True)

    def _metadata(self, obj):
        return obj.metadata_json or {}

    def get_summary(self, obj):
        return obj.name

    def get_probability(self, obj):
        return self._metadata(obj).get("probability")

    def get_impact(self, obj):
        return self._metadata(obj).get("impact")

    def get_severity(self, obj):
        return self._metadata(obj).get("severity")

    def get_impact_area(self, obj):
        return self._metadata(obj).get("impact_area")

    def get_mitigation(self, obj):
        return self._metadata(obj).get("mitigation")

    def get_created_by(self, obj):
        return self._metadata(obj).get("created_by", "system")
