from flask import Flask
from infraestructure.db import engine, Base
from application.routes.cloth_routes import cloth_bp
from application.routes.period_routes import period_bp
from application.routes.status_routes import status_bp
from application.routes.report_routes import report_bp
from application.routes.delivery_date_routes import delivery_date_bp
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
Base.metadata.create_all(bind=engine)

app.register_blueprint(delivery_date_bp)
app.register_blueprint(report_bp)
app.register_blueprint(cloth_bp)
app.register_blueprint(period_bp)
app.register_blueprint(status_bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
