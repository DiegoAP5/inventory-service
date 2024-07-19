from marshmallow import Schema, fields, post_load
from domain.models.period import Period

class PeriodSchema(Schema):
    id = fields.Int(dump_only=True)
    uuid = fields.UUID(dump_only=True)
    start = fields.Date(required=True)
    end = fields.Date(required=True)
    user_id = fields.Int(required=True)
    status_id = fields.Int(required=True)
    clothes = fields.List(fields.Int())
