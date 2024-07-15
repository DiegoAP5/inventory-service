from marshmallow import Schema, fields, validates, ValidationError
from infraestructure.db import SessionLocal
from domain.models.period import Period
from domain.models.status import Status

class ClothSchema(Schema):
    id = fields.Int(dump_only=True)
    uuid = fields.Str(dump_only=True)
    type = fields.Str(required=True)
    image = fields.Str(required=True)
    buy = fields.Float(required=True)
    price = fields.Float(required=True)
    sellPrice = fields.Float(required=True)
    location = fields.Str(required=True)
    description = fields.Str(required=True)
    size = fields.Str(required=True)
    status_id = fields.Int(required=True)
    period_id = fields.Int(required=True)
    created_at = fields.DateTime(dump_only=True)
    sold_at = fields.DateTime(allow_none=True)

    @validates('period_id')
    def validate_period_id(self, value):
        session = SessionLocal()
        period = session.query(Period).filter_by(id=value).first()
        session.close()
        if not period:
            raise ValidationError('Period not found.')

    @validates('status_id')
    def validate_status_id(self, value):
        session = SessionLocal()
        status = session.query(Status).filter_by(id=value).first()
        session.close()
        if not status:
            raise ValidationError('Status not found.')
