from marshmallow import Schema, fields

class ReportSchema(Schema):
    id = fields.Int(dump_only=True)
    uuid = fields.Str(dump_only=True)
    period_id = fields.Int(required=True)
    total_cloth = fields.Int(dump_only=True)
    cloth_selled = fields.Int(dump_only=True)
    cloth_inSell = fields.Int(dump_only=True)
    invest = fields.Float(dump_only=True)
    earnings = fields.Float(dump_only=True)
