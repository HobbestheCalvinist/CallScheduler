# __init__.py
from flask import Flask
from config import Config
from data.models import db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    with app.app_context():
        db.create_all()  # Ensure this is called within the app context

    return app
