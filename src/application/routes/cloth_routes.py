from flask import Blueprint, request
from application.controllers.cloth_controller import ClothController

cloth_bp = Blueprint('cloth', __name__)
controller = ClothController()

@cloth_bp.route('/cloth/create', methods=['POST'])
def create_cloth():
    data = request.json
    response = controller.create_cloth(data)
    return response.to_response()

@cloth_bp.route('/cloth/user/<int:cloth_id>', methods=['GET'])
def get_cloth_and_user_id(cloth_id):
    response = controller.get_cloth_and_user_id_by_cloth_id(cloth_id)
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

@cloth_bp.route('/cloth/delete/<id>', methods=['DELETE'])
def delete_cloth(id):
    response = controller.delete_cloth(id)
    return response.to_response()

@cloth_bp.route('/cloth', methods=['GET'])
def list_clothes():
    response = controller.list_clothes()
    return response.to_response()

@cloth_bp.route('/cloth/prediction/<user_id>', methods=['GET'])
def get_time_series(user_id):
    response = controller.get_sales_prediction(user_id)
    return response.to_response()

@cloth_bp.route('/cloth/period/<period_id>', methods=['GET'])
def get_all_by_period(period_id):
    response = controller.list_cloth_by_period_id(period_id)
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

@cloth_bp.route('/cloth/all/type', methods=['GET'])
def all_cloth_by_status_and_type():
    status_id = request.args.get('status_id')
    type = request.args.get('type')
    response = controller.list_cloth_by_status_and_type(type, status_id)
    return response.to_response()

@cloth_bp.route('/cloth/all/status', methods=['GET'])
def all_cloth_by_status_and_period():
    status_id = request.args.get('status_id')
    response = controller.list_cloth_by_status(status_id)
    return response.to_response()