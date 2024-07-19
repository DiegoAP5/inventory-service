from marshmallow import Schema, fields

class DeliveryDateSchema(Schema):
    id = fields.Int(dump_only=True)
    period_id = fields.Int(required=True)
    date = fields.Str(required=True)
