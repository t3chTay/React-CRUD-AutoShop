from flask import Flask
from app.models import db
from app.extensions import ma


def create_app(config_name=None):
    app = Flask(__name__)

    if config_name == "DevelopmentConfig":
        from config import DevelopmentConfig
        app.config.from_object(DevelopmentConfig)

    db.init_app(app)
    ma.init_app(app)

    from app.blueprints.mechanic import mechanic_bp
    from app.blueprints.service_ticket import service_ticket_bp
    app.register_blueprint(mechanic_bp, url_prefix="/mechanics")
    app.register_blueprint(service_ticket_bp, url_prefix="/service-tickets")

    return app