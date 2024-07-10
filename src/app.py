from flask import Flask
from infraestructure.database.models import create_collections
from infraestructure.ports.api.routes import create_routes
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config.from_object('config.Config')

try:
    mongo = PyMongo(app)
    db = mongo.db
    if db is None:
        raise ValueError("Database connection is not initialized")
    create_collections(db)
    create_routes(app, db)
except Exception as e:
    print(f"Error initializing the database: {e}")

if __name__ == '__main__':
    app.run(debug=True)
