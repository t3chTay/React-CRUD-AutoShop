from flask import Flask
from app.models import db
from app.extensions import ma, limiter, cache
from config import DevelopmentConfig

def create_app(config_name=None):
    app = Flask(__name__)

    if config_name == "DevelopmentConfig":
        
        app.config.from_object(DevelopmentConfig)

    db.init_app(app)
    ma.init_app(app)
    limiter.init_app(app)
    cache.init_app(app)
    

    from app.blueprints.mechanic import mechanic_bp
    from app.blueprints.service_ticket import service_ticket_bp
    from app.blueprints.customers import customers_bp
    from app.blueprints.parts import parts_bp
    app.register_blueprint(mechanic_bp, url_prefix="/mechanics")
    app.register_blueprint(service_ticket_bp, url_prefix="/service-tickets")
    app.register_blueprint(customers_bp, url_prefix="/customers")
    app.register_blueprint(parts_bp, url_prefix="/parts")
    
    return app