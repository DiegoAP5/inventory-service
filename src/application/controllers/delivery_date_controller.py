from domain.models.delivery_date import DeliveryDate
from marshmallow import ValidationError
from infraestructure.repositories.delivery_date_repository import DeliveryDateRepository
from infraestructure.db import SessionLocal
from application.schemas.delivery_date_schema import DeliveryDateSchema
from application.schemas.base_response import BaseResponse
from http import HTTPStatus

class DeliveryDateController:
    def __init__(self):
        self.session = SessionLocal()
        self.repo = DeliveryDateRepository(self.session)
        self.schema = DeliveryDateSchema()

    def create_delivery_date(self, data):
        try:
            delivery_date_data = self.schema.load(data)
            new_delivery_date = DeliveryDate(**delivery_date_data)
            created_delivery_date = self.repo.add(new_delivery_date)
            return BaseResponse(self.to_dict(created_delivery_date), "Delivery Date created successfully", True, HTTPStatus.CREATED)
        except ValidationError as err:
            return BaseResponse(None, str(err), False, HTTPStatus.BAD_REQUEST)

    def get_delivery_date_by_id(self, delivery_date_id):
        delivery_date = self.repo.get_by_id(delivery_date_id)
        if delivery_date:
            return BaseResponse(self.to_dict(delivery_date), "Delivery Date fetched successfully", True, HTTPStatus.OK)
        return BaseResponse(None, "Delivery Date not found", False, HTTPStatus.NOT_FOUND)

    def get_all_delivery_dates_by_period(self, period_id):
        delivery_dates = self.repo.get_all_by_period(period_id)
        return BaseResponse([self.to_dict(dd) for dd in delivery_dates], "Delivery Dates fetched successfully", True, HTTPStatus.OK)

    def update_delivery_date(self, delivery_date_id, data):
        delivery_date = self.repo.get_by_id(delivery_date_id)
        if not delivery_date:
            return BaseResponse(None, "Delivery Date not found", False, HTTPStatus.NOT_FOUND)
        try:
            updated_data = self.schema.load(data, partial=True)
            for key, value in updated_data.items():
                setattr(delivery_date, key, value)
            updated_delivery_date = self.repo.update(delivery_date)
            return BaseResponse(self.to_dict(updated_delivery_date), "Delivery Date updated successfully", True, HTTPStatus.OK)
        except ValidationError as err:
            return BaseResponse(None, str(err), False, HTTPStatus.BAD_REQUEST)

    def delete_delivery_date(self, delivery_date_id):
        delivery_date = self.repo.get_by_id(delivery_date_id)
        if not delivery_date:
            return BaseResponse(None, "Delivery Date not found", False, HTTPStatus.NOT_FOUND)
        self.repo.delete(delivery_date)
        return BaseResponse(None, "Delivery Date deleted successfully", True, HTTPStatus.OK)

    def to_dict(self, delivery_date: DeliveryDate):
        return {
            "id": delivery_date.id,
            "period_id": delivery_date.period_id,
            "date": delivery_date.date
        }
