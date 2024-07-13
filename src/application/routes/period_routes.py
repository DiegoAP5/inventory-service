from flask import Blueprint, request, jsonify
from application.controllers.period_controller import PeriodController

period_bp = Blueprint('period', __name__)
controller = PeriodController()

@period_bp.route('/period', methods=['POST'])
def create_period():
    data = request.json
    new_period = controller.create_period(data)
    return jsonify(controller.to_dict(new_period)), 201

@period_bp.route('/period/<uuid>', methods=['GET'])
def get_period(uuid):
    period = controller.get_period(uuid)
    if period:
        return jsonify(controller.to_dict(period))
    return jsonify({"error": "Period not found"}), 404

@period_bp.route('/period', methods=['GET'])
def get_all_periods():
    periods = controller.get_all_periods()
    return jsonify([controller.to_dict(period) for period in periods])

@period_bp.route('/period/<uuid>', methods=['PUT'])
def update_period(uuid):
    data = request.json
    period = controller.update_period(uuid, data)
    if period:
        return jsonify(controller.to_dict(period))
    return jsonify({"error": "Period not found"}), 404

@period_bp.route('/period/<uuid>', methods=['DELETE'])
def delete_period(uuid):
    controller.delete_period(uuid)
    return '', 204

@period_bp.route('/period/status', methods=['GET'])
def search_period_by_status():
    status_id = request.args.get('status_id')
    periods = controller.search_period_by_status(status_id)
    return jsonify([controller.to_dict(period) for period in periods])
