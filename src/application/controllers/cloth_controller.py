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
        try:
            # Obtener datos de la base de datos
            cloth_data = self.repo.get_to_statics(user_id)

            # Procesar datos
            data = [{'date': cloth.selled_date, 'quantity': 1} for cloth in cloth_data]
            df = pd.DataFrame(data)

            # Asegurarse de que la fecha está en el formato correcto
            df['date'] = pd.to_datetime(df['date'])
            df = df.set_index('date')
            
            # Agrupar por día y contar las ventas
            daily_sales = df.resample('D').sum().fillna(0)

            # Aplicar suavizado exponencial
            daily_sales['forecast'] = daily_sales['quantity'].ewm(span=30, adjust=False).mean()

            # Preparar la respuesta
            response_data = daily_sales.reset_index().to_dict(orient='records')

            return BaseResponse(response_data, "Time series data retrieved successfully.", True, HTTPStatus.OK)

        except Exception as e:
            return BaseResponse(None, "Error during prediction", False, HTTPStatus.CONFLICT)

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
    
    def get_cloth_and_user_id_by_cloth_id(self, cloth_id):
        try:
        # Consulta para obtener los datos de la ropa y el user_id a partir del cloth_id
            result = self.repo.get_cloth_and_user_id(cloth_id)

            if result:
                cloth, user_id = result
                response_data = {
                    'cloth': {
                        'id': cloth.id,
                        'uuid': cloth.uuid,
                        'period_id': cloth.period_id,
                        'type': cloth.type,
                        'buy': cloth.buy,
                        'sellPrice': cloth.sellPrice,
                        'sold_at': cloth.sold_at,
                        'status_id': cloth.status_id,
                        'created_at': cloth.created_at
                    },
                    'user_id': user_id
                }
                return BaseResponse(response_data, "Cloth data and User ID retrieved successfully.", True, HTTPStatus.OK)
            else:
                return BaseResponse(None, "Cloth ID not found.", False, HTTPStatus.NOT_FOUND)
            
        except Exception as e:
            return BaseResponse(None, "Error", False, 500)

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
