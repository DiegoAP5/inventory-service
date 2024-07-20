from marshmallow import ValidationError
from domain.models.cloth import Cloth
from infraestructure.repositories.cloth_repository import ClothRepository
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from infraestructure.db import SessionLocal
from domain.models.cloth import Cloth
from application.schemas.cloth_schema import ClothSchema
from application.schemas.base_response import BaseResponse
from http import HTTPStatus
import pandas as pd

class ClothController:
    def __init__(self):
        self.session = SessionLocal()
        self.repo = ClothRepository(self.session)
        self.schema = ClothSchema()

    def create_cloth(self, data):
        try:
            validated_data = self.schema.load(data)
            new_cloth = Cloth(**validated_data)
            self.repo.add(new_cloth)
            return BaseResponse(self.to_dict(new_cloth), "Cloth created successfully", True, HTTPStatus.CREATED)
        except ValidationError as err:
            return BaseResponse(None, err.messages, False, HTTPStatus.BAD_REQUEST)
        
    def get_sales_prediction(self, user_id):
        sales_data = self.repo.get_to_statics(user_id)
        
        if not sales_data:
            return BaseResponse(None, "No sales data available", False, 404)
        
        df = pd.DataFrame([{
            'date': cloth.sold_at,
            'quantity': cloth.quantity
        } for cloth in sales_data])
        
        if df.empty:
            return BaseResponse(None, "No sales data available", False, 404)
        
        # Asegurarse de que las fechas estén ordenadas
        df = df.sort_values('date')
        df.set_index('date', inplace=True)

        # Crear serie de tiempo sumando las cantidades vendidas por día
        daily_sales = df.resample('D').sum()

        # Aplicar suavizado exponencial
        model = ExponentialSmoothing(daily_sales['quantity'], trend='add', seasonal='add', seasonal_periods=7)
        fit = model.fit()

        # Predicciones
        forecast = fit.forecast(steps=30)  # Predicción para los próximos 30 días

        # Preparar los datos para la respuesta
        response_data = {
            'historical': daily_sales.to_dict(),
            'forecast': forecast.to_dict()
        }
        
        return BaseResponse(response_data, "Sales prediction data retrieved successfully", True, 200).__dict__

    def update_cloth(self, uuid, data):
        cloth = self.repo.get_by_uuid(uuid)
        if cloth:
            try:
                validated_data = self.schema.load(data, partial=True)
                for key, value in validated_data.items():
                    setattr(cloth, key, value)
                self.repo.update(cloth)
                return BaseResponse(self.to_dict(cloth), "Cloth updated successfully", True, HTTPStatus.OK)
            except ValidationError as err:
                return BaseResponse(None, err.messages, False, HTTPStatus.BAD_REQUEST)
        return BaseResponse(None, "Cloth not found", False, HTTPStatus.NOT_FOUND)

    def get_cloth(self, uuid):
        cloth = self.repo.get_by_uuid(uuid)
        if cloth:
            return BaseResponse(self.to_dict(cloth), "Cloth fetched successfully", True, HTTPStatus.OK)
        return BaseResponse(None, "Cloth not found", False, HTTPStatus.NOT_FOUND)

    def delete_cloth(self, uuid):
        cloth = self.repo.get_by_uuid(uuid)
        if cloth:
            self.repo.delete(cloth)
            return BaseResponse(None, "Cloth deleted successfully", True, HTTPStatus.NO_CONTENT)
        return BaseResponse(None, "Cloth not found", False, HTTPStatus.NOT_FOUND)

    def list_clothes(self):
        clothes = self.repo.get_all()
        return BaseResponse([self.to_dict(cloth) for cloth in clothes], "Clothes fetched successfully", True, HTTPStatus.OK)
    
    def search_cloth_by_type_and_period(self, type, period_id):
        cloth = self.repo.search_by_type_and_period(type, period_id)
        if cloth:
            return BaseResponse([self.to_dict(cloth) for cloth in cloth], "Cloth fetched successfully", True, HTTPStatus.OK)
        return BaseResponse(None, "Cloth not found", False, HTTPStatus.NOT_FOUND)

    def list_cloth_by_status_and_period(self, status_id, period_id):
        cloth = self.repo.list_by_status_and_period(status_id, period_id)
        if cloth:
            return BaseResponse([self.to_dict(cloth) for cloth in cloth], "Clothes fetched", True, HTTPStatus.OK)
        return BaseResponse(None, "Clothes not found", False, HTTPStatus.NOT_FOUND)

    def to_dict(self, cloth: Cloth):
        return {
            "id": cloth.id,
            "uuid": cloth.uuid,
            "type": cloth.type,
            "image": cloth.image,
            "buy": cloth.buy,
            "price": cloth.price,
            "sellPrice": cloth.sellPrice,
            "location": cloth.location,
            "description": cloth.description,
            "size": cloth.size,
            "status_id": cloth.status_id,
            "period_id": cloth.period_id,
            "created_at": cloth.created_at,
            "sold_at": cloth.sold_at
        }
