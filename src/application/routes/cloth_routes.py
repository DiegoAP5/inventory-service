from flask import Blueprint, request
from application.controllers.cloth_controller import ClothController

cloth_bp = Blueprint('cloth', __name__)
controller = ClothController()

@cloth_bp.route('/cloth/create', methods=['POST'])
def create_cloth():
    data = request.json
    response = controller.create_cloth(data)
    return response.to_response()

@cloth_bp.route('/cloth/update/<uuid>', methods=['PUT'])
def update_cloth(uuid):
    data = request.json
    response = controller.update_cloth(uuid, data)
    return response.to_response()

@cloth_bp.route('/cloth/<uuid>', methods=['GET'])
def get_cloth(uuid):
    response = controller.get_cloth(uuid)
    return response.to_response()

@cloth_bp.route('/cloth/delete/<uuid>', methods=['DELETE'])
def delete_cloth(uuid):
    response = controller.delete_cloth(uuid)
    return response.to_response()

@cloth_bp.route('/cloth', methods=['GET'])
def list_clothes():
    response = controller.list_clothes()
    return response.to_response()

@cloth_bp.route('/cloth/search', methods=['GET'])
def search_cloth_by_type_and_period():
    type = request.args.get('type')
    period_id = request.args.get('period_id')
    response = controller.search_cloth_by_type_and_period(type, period_id)
    return response.to_response()

@cloth_bp.route('/cloth/status', methods=['GET'])
def list_cloth_by_status_and_period():
    status_id = request.args.get('status_id')
    period_id = request.args.get('period_id')
    response = controller.list_cloth_by_status_and_period(status_id, period_id)
    return response.to_response()
