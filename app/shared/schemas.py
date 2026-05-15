from marshmallow import Schema, ValidationError, fields


def non_empty(value):
    if value is None or not str(value).strip():
        raise ValidationError("Field must not be empty")


def load_json(schema: Schema, data: dict):
    return schema.load(data or {})


class GovernanceResponseSchema(Schema):
    id = fields.String(required=True)
    status = fields.String(required=True)
    created_at = fields.DateTime(required=True)
    updated_at = fields.DateTime(required=True)
    version = fields.Integer(required=True)
    created_by = fields.String(required=True)
