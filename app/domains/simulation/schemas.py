from marshmallow import Schema, fields


class SimulationRunResponseSchema(Schema):
    id = fields.String(required=True)
    scenario_id = fields.String(required=True)
    total_processing_hours = fields.Float(required=True)
    total_cost = fields.Float(required=True)
    deterministic_formula = fields.String(required=True)
    simulated_at = fields.DateTime(required=True)
    impact_assessment_id = fields.Method("get_impact_assessment_id")
    status = fields.String(required=True)
    created_at = fields.DateTime(required=True)
    updated_at = fields.DateTime(required=True)
    version = fields.Integer(required=True)
    created_by = fields.String(required=True)

    def get_impact_assessment_id(self, obj):
        return obj.impact_assessment.id if obj.impact_assessment else None
