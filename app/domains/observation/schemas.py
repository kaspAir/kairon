from marshmallow import Schema, fields


class ObservationCreateSchema(Schema):
    expected_benefit = fields.Float(required=True)
    actual_benefit = fields.Float(required=True)
    expected_cost = fields.Float(required=True)
    actual_cost = fields.Float(required=True)
    expected_risks = fields.String(load_default=None, allow_none=True)
    actual_risks = fields.String(load_default=None, allow_none=True)
    comment = fields.String(load_default=None, allow_none=True)
    observed_at = fields.DateTime(load_default=None, allow_none=True)
    created_by = fields.String(load_default="system")


class ObservationResponseSchema(Schema):
    id = fields.String()
    decision_id = fields.String()
    expected_benefit = fields.Float()
    actual_benefit = fields.Float()
    expected_cost = fields.Float()
    actual_cost = fields.Float()
    expected_risks = fields.String(allow_none=True)
    actual_risks = fields.String(allow_none=True)
    comment = fields.String(allow_none=True)
    observed_at = fields.DateTime()
    status = fields.String()
    created_by = fields.String()
