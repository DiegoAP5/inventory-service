from flask import Flask
from infraestructure.db import engine, Base
from application.routes.api import api_bp
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
Base.metadata.create_all(bind=engine)

app.register_blueprint(api_bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
