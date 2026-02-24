from app.models import Mechanic
from flask_marshmallow.sqla import SQLAlchemyAutoSchema
from app.extensions import ma
from marshmallow import Schema, fields


class MechanicSchema(ma.SQLAlchemyAutoSchema):
    
    password = fields.String(load_only=True, required=True)
    class Meta:
        model = Mechanic
        load_instance = True
        include_fk = True
mechanic_schema = MechanicSchema()
mechanics_schema = MechanicSchema(many=True)

class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True)