from marshmallow import Schema, fields, validate

class ReportSchema(Schema):
    uuid = fields.UUID(dump_only=True)
    period_id = fields.Integer(required=True)
    total_cloth = fields.Integer(dump_only=True)
    cloth_selled = fields.Integer(dump_only=True)
    cloth_inSell = fields.Integer(dump_only=True)
    invest = fields.Integer(dump_only=True)
    earnings = fields.Integer(dump_only=True)
