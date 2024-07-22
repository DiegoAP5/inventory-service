from marshmallow import ValidationError
from domain.models.cloth import Cloth
from infraestructure.repositories.cloth_repository import ClothRepository
from infraestructure.db import SessionLocal
from domain.models.cloth import Cloth
import xgboost as xgb
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from application.schemas.cloth_schema import ClothSchema
from application.schemas.base_response import BaseResponse
from http import HTTPStatus
from datetime import timedelta

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
            cloth_data = self.repo.get_to_statics(user_id)

            if not cloth_data:
                return BaseResponse(None, "No sales data found for the specified user.", False, HTTPStatus.BAD_REQUEST)

            data = [{'date': cloth.sold_at, 'quantity': 1} for cloth in cloth_data if cloth.sold_at is not None]
            
            if not data:
                return BaseResponse(None, "No valid sales dates found for the specified user.", False, HTTPStatus.BAD_REQUEST)

            df = pd.DataFrame(data)

            df['date'] = pd.to_datetime(df['date'], errors='coerce')
            df = df.dropna(subset=['date'])
            df = df.set_index('date')

            if df.empty:
                return BaseResponse(None, "No valid sales data after filtering dates.", False, HTTPStatus.BAD_REQUEST)

            daily_sales = df.resample('D').sum().fillna(0)

            if daily_sales.empty:
                return BaseResponse(None, "No sales data after resampling.", False, HTTPStatus.BAD_REQUEST)

            daily_sales['day_of_year'] = daily_sales.index.dayofyear
            daily_sales['day_of_week'] = daily_sales.index.dayofweek
            daily_sales['week_of_year'] = daily_sales.index.isocalendar().week

            X = daily_sales[['day_of_year', 'day_of_week', 'week_of_year']]
            y = daily_sales['quantity']

            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

            model = xgb.XGBRegressor(objective='reg:squarederror', n_estimators=100, learning_rate=0.1)
            model.fit(X_train, y_train)

            y_pred = model.predict(X_test)

            rmse = np.sqrt(mean_squared_error(y_test, y_pred))

            last_date = daily_sales.index[-1]
            forecast_dates = [last_date + timedelta(days=i) for i in range(1, 6)]
            forecast_data = pd.DataFrame({
                'day_of_year': [date.dayofyear for date in forecast_dates],
                'day_of_week': [date.dayofweek for date in forecast_dates],
                'week_of_year': [date.isocalendar().week for date in forecast_dates]
            })

            forecast_values = model.predict(forecast_data)

            forecast_df = pd.DataFrame({
                'date': forecast_dates,
                'quantity': [None] * 5,
                'forecast': forecast_values
            }).set_index('date')

            combined_df = pd.concat([daily_sales, forecast_df])

            response_data = combined_df.reset_index().to_dict(orient='records')

            return BaseResponse(response_data, "Time series data retrieved and forecasted successfully.", True, HTTPStatus.OK)

        except Exception as e:
            return BaseResponse(None, f"An error occurred: {str(e)}", False, HTTPStatus.BAD_REQUEST)

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

    def delete_cloth(self, id):
        cloth = self.repo.delete(id)
        return BaseResponse(cloth, "Cloth deleted", True, HTTPStatus.OK)

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
                        'created_at': cloth.created_at,
                        'user_id': user_id
                    },
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
    
    def list_cloth_by_status_and_type(self, type, status_id):
        cloth = self.repo.get_all_by_status_and_type(type, status_id)
        if cloth:
            return BaseResponse([self.to_dict(cloth) for cloth in cloth], "Clothes fetched", True, HTTPStatus.OK)
        return BaseResponse(None, "Clothes not found", False, HTTPStatus.NOT_FOUND)
    
    def list_cloth_by_status(self, status_id):
        cloth = self.repo.get_all_by_status(status_id)
        if cloth:
            return BaseResponse([self.to_dict(cloth) for cloth in cloth], "Clothes fetched", True, HTTPStatus.OK)
        return BaseResponse(None, "Clothes not found", False, HTTPStatus.NOT_FOUND)
    
    def list_cloth_by_period_id(self, period_id):
        cloth = self.repo.get_all_by_period(period_id)
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
