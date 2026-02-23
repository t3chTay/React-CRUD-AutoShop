from app.extensions import ma
from flask_marshmallow.sqla import SQLAlchemyAutoSchema
from marshmallow import fields
from app.models import ServiceTickets, Mechanic

class MechanicNestedSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Mechanic
        load_instance = True
        include_fk = True

class ServiceTicketSchema(SQLAlchemyAutoSchema):
    mechanics = fields.Nested(MechanicNestedSchema, many=True)

    class Meta:
        model = ServiceTickets
        load_instance = True
        include_fk = True


service_ticket_schema = ServiceTicketSchema()
service_tickets_schema = ServiceTicketSchema(many=True)