from flask import Blueprint, request, jsonify
from application.controllers.status_controller import StatusController

status_bp = Blueprint('status', __name__)
controller = StatusController()

@status_bp.route('/status', methods=['POST'])
def create_status():
    data = request.json
    new_status = controller.create_status(data)
    return jsonify(controller.to_dict(new_status)), 201

@status_bp.route('/status/<uuid>', methods=['GET'])
def get_status(uuid):
    status = controller.get_status(uuid)
    if status:
        return jsonify(controller.to_dict(status))
    return jsonify({"error": "Status not found"}), 404

@status_bp.route('/status', methods=['GET'])
def get_all_statuses():
    statuses = controller.get_all_statuses()
    return jsonify([controller.to_dict(status) for status in statuses])

@status_bp.route('/status/<uuid>', methods=['PUT'])
def update_status(uuid):
    data = request.json
    status = controller.update_status(uuid, data)
    if status:
        return jsonify(controller.to_dict(status))
    return jsonify({"error": "Status not found"}), 404

@status_bp.route('/status/<uuid>', methods=['DELETE'])
def delete_status(uuid):
    controller.delete_status(uuid)
    return '', 204
