from flask import Flask
from infraestructure.db import engine, Base
from application.routes.api import api_bp
import threading
from application.services.consumer import start_consuming 

app = Flask(__name__)
Base.metadata.create_all(bind=engine)

app.register_blueprint(api_bp)

if __name__ == '__main__':
    consumer_thread = threading.Thread(target=start_consuming)
    consumer_thread.start()
    app.run(host='0.0.0.0', port=5000)
