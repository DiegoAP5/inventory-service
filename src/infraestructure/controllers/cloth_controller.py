from flask import jsonify
from application.services.cloth_service import ClothService
from infraestructure.database.repositories import ClothRepository

class ClothController:
    def __init__(self, mongo):
        self.cloth_service = ClothService(ClothRepository(mongo))

    def create_cloth(self, data):
        result = self.cloth_service.create(data)
        return jsonify({"msg": "Cloth created", "id": str(result.inserted_id)}), 201

    def get_cloth(self, id):
        cloth = self.cloth_service.get_by_id(id)
        if cloth:
            return jsonify(cloth), 200
        return jsonify({"msg": "Cloth not found"}), 404

    def update_cloth(self, id, data):
        result = self.cloth_service.update(id, data)
        if result.matched_count:
            return jsonify({"msg": "Cloth updated"}), 200
        return jsonify({"msg": "Cloth not found"}), 404

    def delete_cloth(self, id):
        result = self.cloth_service.delete(id)
        if result.deleted_count:
            return jsonify({"msg": "Cloth deleted"}), 200
        return jsonify({"msg": "Cloth not found"}), 404

    def get_cloth_by_type(self, cloth_type):
        cloths = self.cloth_service.find_by_type(cloth_type)
        return jsonify([cloth for cloth in cloths]), 200

    def get_cloth_by_status(self, status):
        cloths = self.cloth_service.find_by_status(status)
        return jsonify([cloth for cloth in cloths]), 200
