from flask import Flask
from infraestructure.database import engine, Base
from application.routes.cloth_routes import cloth_bp
from application.routes.period_routes import period_bp
from application.routes.status_routes import status_bp

app = Flask(__name__)

# Crear todas las tablas en la base de datos
Base.metadata.create_all(bind=engine)

# Registrar Blueprints
app.register_blueprint(cloth_bp)
app.register_blueprint(period_bp)
app.register_blueprint(status_bp)

if __name__ == '__main__':
    app.run(debug=True)