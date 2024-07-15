from flask import Blueprint, request
from application.controllers.period_controller import PeriodController

period_bp = Blueprint('period', __name__)
controller = PeriodController()

@period_bp.route('/period', methods=['POST'])
def create_period():
    data = request.json
    response = controller.create_period(data)
    return response.to_response()

@period_bp.route('/period/<uuid>', methods=['PUT'])
def update_period(uuid):
    data = request.json
    response = controller.update_period(uuid, data)
    return response.to_response()

@period_bp.route('/period/<uuid>', methods=['GET'])
def get_period(uuid):
    response = controller.get_period(uuid)
    return response.to_response()

@period_bp.route('/period/<uuid>', methods=['DELETE'])
def delete_period(uuid):
    response = controller.delete_period(uuid)
    return response.to_response()

@period_bp.route('/periods', methods=['GET'])
def list_periods():
    response = controller.list_periods()
    return response.to_response()


@period_bp.route('/period/status', methods=['GET'])
def search_period_by_status():
    status_id = request.args.get('status_id')
    response = controller.search_period_by_status(status_id)
    return response.to_response()
