from flask import Blueprint, request
from application.controllers.delivery_date_controller import DeliveryDateController

delivery_date_bp = Blueprint('delivery_date', __name__)
controller = DeliveryDateController()

@delivery_date_bp.route('/delivery_date/create', methods=['POST'])
def create_delivery_date():
    data = request.get_json()
    response = controller.create_delivery_date(data)
    return response.to_response()

@delivery_date_bp.route('/delivery_date/<int:delivery_date_id>', methods=['GET'])
def get_delivery_date_by_id(delivery_date_id):
    response = controller.get_delivery_date_by_id(delivery_date_id)
    return response.to_response()

@delivery_date_bp.route('/delivery_date/period/<int:period_id>', methods=['GET'])
def get_all_delivery_dates_by_period(period_id):
    response = controller.get_all_delivery_dates_by_period(period_id)
    return response.to_response()

@delivery_date_bp.route('/delivery_date/update/<int:delivery_date_id>', methods=['PUT'])
def update_delivery_date(delivery_date_id):
    data = request.get_json()
    response = controller.update_delivery_date(delivery_date_id, data)
    return response.to_response()

@delivery_date_bp.route('/delivery_date/delete/<int:delivery_date_id>', methods=['DELETE'])
def delete_delivery_date(delivery_date_id):
    response = controller.delete_delivery_date(delivery_date_id)
    return response.to_response()
