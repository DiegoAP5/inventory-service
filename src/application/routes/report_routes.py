from flask import Blueprint, request
from application.controllers.report_controller import ReportController

report_bp = Blueprint('report', __name__)
controller = ReportController()

@report_bp.route('/report', methods=['POST'])
def create_report():
    data = request.json
    response = controller.create_report(data)
    return response.to_response()

@report_bp.route('/report/<uuid>', methods=['PUT'])
def update_report(uuid):
    data = request.json
    response = controller.update_report(uuid, data)
    return response.to_response()

@report_bp.route('/report/<uuid>', methods=['GET'])
def get_report(uuid):
    response = controller.get_report(uuid)
    return response.to_response()

@report_bp.route('/report/<uuid>', methods=['DELETE'])
def delete_report(uuid):
    response = controller.delete_report(uuid)
    return response.to_response()

@report_bp.route('/reports', methods=['GET'])
def list_reports():
    response = controller.list_reports()
    return response.to_response()
