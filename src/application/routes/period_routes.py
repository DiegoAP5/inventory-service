from flask import Blueprint, request
from application.controllers.period_controller import PeriodController

period_bp = Blueprint('period', __name__)
controller = PeriodController()

@period_bp.route('/period/create', methods=['POST'])
def create_period():
    data = request.json
    response = controller.create_period(data)
    return response.to_response()

@period_bp.route('/period/update/<uuid>', methods=['PUT'])
def update_period(uuid):
    data = request.json
    response = controller.update_period(uuid, data)
    return response.to_response()

@period_bp.route('/period/<uuid>', methods=['GET'])
def get_period(uuid):
    response = controller.get_period(uuid)
    return response.to_response()

@period_bp.route('/period/user/<id>', methods=['GET'])
def get_period_by_user_id(id):
    response = controller.get_period_by_user_id(id)
    return response.to_response()

@period_bp.route('/period/delete/<uuid>', methods=['DELETE'])
def delete_period(uuid):
    response = controller.delete_period(uuid)
    return response.to_response()

@period_bp.route('/period', methods=['GET'])
def list_periods():
    response = controller.list_periods()
    return response.to_response()


@period_bp.route('/period/status/<status_id>/user/<user_id>', methods=['GET'])
def search_period_by_status(status_id,user_id):
    response = controller.get_periods_by_status(status_id,user_id)
    return response.to_response()
