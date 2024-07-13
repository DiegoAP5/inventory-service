from flask import Blueprint, request, jsonify
from application.controllers.cloth_controller import ClothController

cloth_bp = Blueprint('cloth', __name__)
controller = ClothController()

@cloth_bp.route('/cloth', methods=['POST'])
def create_cloth():
    data = request.json
    new_cloth = controller.create_cloth(data)
    return jsonify(controller.to_dict(new_cloth)), 201

@cloth_bp.route('/cloth/<uuid>', methods=['GET'])
def get_cloth(uuid):
    cloth = controller.get_cloth(uuid)
    if cloth:
        return jsonify(controller.to_dict(cloth))
    return jsonify({"error": "Cloth not found"}), 404

@cloth_bp.route('/cloth', methods=['GET'])
def get_all_clothes():
    clothes = controller.get_all_clothes()
    return jsonify([controller.to_dict(cloth) for cloth in clothes])

@cloth_bp.route('cloth/<uuid>', methods=['PUT'])
def update_cloth(uuid):
    data = request.json
    cloth = controller.update_cloth(uuid, data)
    if cloth:
        return jsonify(controller.to_dict(cloth))
    return jsonify({"error": "Cloth not found"}), 404

@cloth_bp.route('/cloth/<uuid>', methods=['DELETE'])
def delete_cloth(uuid):
    controller.delete_cloth(uuid)
    return '', 204

@cloth_bp.route('/cloth/search', methods=['GET'])
def search_cloth_by_type_and_period():
    type = request.args.get('type')
    period_id = request.args.get('period_id')
    clothes = controller.search_cloth_by_type_and_period(type, period_id)
    return jsonify([controller.to_dict(cloth) for cloth in clothes])

@cloth_bp.route('/cloth/status', methods=['GET'])
def list_cloth_by_status_and_period():
    status_id = request.args.get('status_id')
    period_id = request.args.get('period_id')
    clothes = controller.list_cloth_by_status_and_period(status_id, period_id)
    return jsonify([controller.to_dict(cloth) for cloth in clothes])
