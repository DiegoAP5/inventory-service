from flask import Blueprint
from application.routes import cloth_routes, period_routes, status_routes, report_routes, delivery_date_routes

api_bp = Blueprint('api', __name__, url_prefix='/api')

# Registrar los Blueprints individuales con el Blueprint general
api_bp.register_blueprint(cloth_routes.cloth_bp)
api_bp.register_blueprint(period_routes.period_bp)
api_bp.register_blueprint(status_routes.status_bp)
api_bp.register_blueprint(report_routes.report_bp)
api_bp.register_blueprint(delivery_date_routes.delivery_date_bp)
