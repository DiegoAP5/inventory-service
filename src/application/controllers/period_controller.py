from marshmallow import ValidationError
from domain.models.period import Period
from infraestructure.repositories.period_repository import PeriodRepository
from infraestructure.db import SessionLocal
from application.schemas.period_schema import PeriodSchema
from application.schemas.base_response import BaseResponse
from http import HTTPStatus

class PeriodController:
    def __init__(self):
        self.session = SessionLocal()
        self.repo = PeriodRepository(self.session)
        self.schema = PeriodSchema()

    def create_period(self, data):
        try:
            validated_data = self.schema.load(data)
            new_period = Period(**validated_data)
            self.repo.add(new_period)
            return BaseResponse(self.to_dict(new_period), "Period created successfully", True, HTTPStatus.CREATED)
        except ValidationError as err:
            return BaseResponse(None, err.messages, False, HTTPStatus.BAD_REQUEST)

    def update_period(self, uuid, data):
        period = self.repo.get_by_uuid(uuid)
        if period:
            try:
                validated_data = self.schema.load(data, partial=True)
                for key, value in validated_data.items():
                    setattr(period, key, value)
                self.repo.update(period)
                return BaseResponse(self.to_dict(period), "Period updated successfully", True, HTTPStatus.OK)
            except ValidationError as err:
                return BaseResponse(None, err.messages, False, HTTPStatus.BAD_REQUEST)
        return BaseResponse(None, "Period not found", False, HTTPStatus.NOT_FOUND)

    def get_period(self, uuid):
        period = self.repo.get_by_uuid(uuid)
        if period:
            return BaseResponse(self.to_dict(period), "Period fetched successfully", True, HTTPStatus.OK)
        return BaseResponse(None, "Period not found", False, HTTPStatus.NOT_FOUND)

    def delete_period(self, uuid):
        period = self.repo.get_by_uuid(uuid)
        if period:
            self.repo.delete(period)
            return BaseResponse(None, "Period deleted successfully", True, HTTPStatus.NO_CONTENT)
        return BaseResponse(None, "Period not found", False, HTTPStatus.NOT_FOUND)

    def list_periods(self):
        periods = self.repo.get_all()
        return BaseResponse([self.to_dict(period) for period in periods], "Periods fetched successfully", True, HTTPStatus.OK)

    def get_periods_by_status(self, status_id):
        periods = self.repo.get_by_status(status_id)
        return BaseResponse([self.to_dict(period) for period in periods], "Periods fetched successfully", True, HTTPStatus.OK)

    def to_dict(self, period: Period):
        return {
            "id": period.id,
            "uuid": period.uuid,
            "start": period.start,
            "end": period.end,
            "status_id": period.status_id,
            "clothes": [cloth.id for cloth in period.clothes]
        }
