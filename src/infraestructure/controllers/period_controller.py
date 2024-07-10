from flask import jsonify
from application.services.period_service import PeriodService
from infraestructure.database.repositories import PeriodRepository

class PeriodController:
    def __init__(self, mongo):
        self.period_service = PeriodService(PeriodRepository(mongo))

    def create_period(self, data):
        result = self.period_service.create(data)
        return jsonify({"msg": "Period created", "id": str(result.inserted_id)}), 201

    def get_period(self, id):
        period = self.period_service.get_by_id(id)
        if period:
            return jsonify(period), 200
        return jsonify({"msg": "Period not found"}), 404

    def update_period(self, id, data):
        result = self.period_service.update(id, data)
        if result.matched_count:
            return jsonify({"msg": "Period updated"}), 200
        return jsonify({"msg": "Period not found"}), 404

    def delete_period(self, id):
        result = self.period_service.delete(id)
        if result.deleted_count:
            return jsonify({"msg": "Period deleted"}), 200
        return jsonify({"msg": "Period not found"}), 404

    def get_period_cloth_count(self, id):
        count = self.period_service.get_cloth_count(id)
        return jsonify({"count": count}), 200

    def get_period_cloth_list(self, id):
        cloths = self.period_service.get_cloth_list(id)
        return jsonify([cloth for cloth in cloths]), 200
