from flask import jsonify
from application.services.status_service import StatusService
from infraestructure.database.repositories import StatusRepository

class StatusController:
    def __init__(self, mongo):
        self.status_service = StatusService(StatusRepository(mongo))

    def create_status(self, data):
        result = self.status_service.create(data)
        return jsonify({"msg": "Status created", "id": str(result.inserted_id)}), 201

    def get_status(self, id):
        status = self.status_service.get_by_id(id)
        if status:
            return jsonify(status), 200
        return jsonify({"msg": "Status not found"}), 404

    def update_status(self, id, data):
        result = self.status_service.update(id, data)
        if result.matched_count:
            return jsonify({"msg": "Status updated"}), 200
        return jsonify({"msg": "Status not found"}), 404

    def delete_status(self, id):
        result = self.status_service.delete(id)
        if result.deleted_count:
            return jsonify({"msg": "Status deleted"}), 200
        return jsonify({"msg": "Status not found"}), 404
