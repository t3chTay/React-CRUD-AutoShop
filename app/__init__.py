from flask import Flask, jsonify
from app.models import db
from app.extensions import ma, limiter, cache
from config import DevelopmentConfig, ProductionConfig
from flask_swagger import swagger
from flask_swagger_ui import get_swaggerui_blueprint
from marshmallow.exceptions import ValidationError

# def create_app(config_name=None):
#     app = Flask(__name__)

#     if config_name == "DevelopmentConfig":
        
#         app.config.from_object(DevelopmentConfig)

#     db.init_app(app)
#     ma.init_app(app)
#     limiter.init_app(app)
#     cache.init_app(app)
    

#     from app.blueprints.mechanic import mechanic_bp
#     from app.blueprints.service_ticket import service_ticket_bp
#     from app.blueprints.customers import customers_bp
#     from app.blueprints.parts import parts_bp
#     app.register_blueprint(mechanic_bp, url_prefix="/mechanics")
#     app.register_blueprint(service_ticket_bp, url_prefix="/service-tickets")
#     app.register_blueprint(customers_bp, url_prefix="/customers")
#     app.register_blueprint(parts_bp, url_prefix="/parts")
    
#     @app.get("/swagger.json")
#     def swagger_spec():
#         swag = swagger(app)
#         swag["info"]["title"] = "Auto Shop API"
#         swag["info"]["version"] = "1.0"

#         swag["securityDefinitions"] = {
#             "BearerAuth": {
#                 "type": "apiKey",
#                 "name": "Authorization",
#                 "in": "header",
#                 "description": "Enter: Bearer <your_token>"
#             }
#         }

#         return jsonify(swag)

#     SWAGGER_URL = "/docs"
#     API_URL = "/swagger.json"

#     swagger_ui_blueprint = get_swaggerui_blueprint(
#         SWAGGER_URL,
#         API_URL,
#         config={"app_name": "Auto Shop API"}
#     )

#     app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)        
    
#     @app.errorhandler(ValidationError)
#     def handle_marshmallow_validation(err):
#         return jsonify({"errors": err.messages}), 400
    
#     return app


def create_app(config_name=None):
    app = Flask(__name__)

    if config_name == "ProductionConfig":
        app.config.from_object(ProductionConfig)
    else:
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
    
    @app.get("/")
    def home():
        return {"message": "Auto Shop API is running", "docs": "/docs"}, 200
    @app.get("/swagger.json")
    def swagger_spec():
        swag = swagger(app)
        swag["info"]["title"] = "Auto Shop API"
        swag["info"]["version"] = "1.0"

        swag["securityDefinitions"] = {
            "BearerAuth": {
                "type": "apiKey",
                "name": "Authorization",
                "in": "header",
                "description": "Enter: Bearer <your_token>"
            }
        }
        return jsonify(swag)

    SWAGGER_URL = "/docs"
    API_URL = "/swagger.json"

    swagger_ui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={"app_name": "Auto Shop API"}
    )

    app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)     
    
    @app.errorhandler(ValidationError)
    def handle_marshmallow_validation(err):
        return jsonify ({"errors": err.messages}), 400   
    

    return app