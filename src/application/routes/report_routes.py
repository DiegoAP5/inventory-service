from flask import Blueprint, request
from application.controllers.report_controller import ReportController

report_bp = Blueprint('report', __name__)
controller = ReportController()

@report_bp.route('/report', methods=['POST'])
def create_or_update_report():
    data = request.json
    response = controller.create_or_update_report(data)
    return response.to_response()

@report_bp.route('/report/<int:period_id>', methods=['GET'])
def get_report_by_period(period_id):
    response = controller.get_report_by_period(period_id)
    return response.to_response()
