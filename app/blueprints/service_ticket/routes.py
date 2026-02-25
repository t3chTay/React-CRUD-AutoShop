from flask import request, abort
from sqlalchemy import select
from app.models import db, ServiceTickets, Mechanic, Inventory, Part
from . import service_ticket_bp
from .schemas import ServiceTicketSchema

ticket_schema = ServiceTicketSchema()
tickets_schema = ServiceTicketSchema(many=True)

@service_ticket_bp.post("/")
def create_ticket():
    data = request.get_json() or {}

    required = ["customer_id", "service_desc", "VIN", "service_date", "price"]
    missing = [f for f in required if f not in data]
    if missing:
        return {"error": f"Missing required fields: {missing}"}, 400

    ticket = ticket_schema.load(data)
    db.session.add(ticket)
    db.session.commit()
    return ticket_schema.jsonify(ticket), 201


@service_ticket_bp.get("/")
def get_tickets():
    tickets = db.session.scalars(select(ServiceTickets)).all()
    return tickets_schema.jsonify(tickets), 200


@service_ticket_bp.put("/<int:ticket_id>/assign-mechanic/<int:mechanic_id>")
def assign_mechanic(ticket_id, mechanic_id):
    ticket = db.session.get(ServiceTickets, ticket_id)
    if not ticket:
        abort(404, description="Service ticket not found")

    mechanic = db.session.get(Mechanic, mechanic_id)
    if not mechanic:
        abort(404, description="Mechanic not found")

    if mechanic not in ticket.mechanics:
        ticket.mechanics.append(mechanic)
        db.session.commit()

    return ticket_schema.jsonify(ticket), 200


@service_ticket_bp.put("/<int:ticket_id>/remove-mechanic/<int:mechanic_id>")
def remove_mechanic(ticket_id, mechanic_id):
    ticket = db.session.get(ServiceTickets, ticket_id)
    if not ticket:
        abort(404, description="Service ticket not found")

    mechanic = db.session.get(Mechanic, mechanic_id)
    if not mechanic:
        abort(404, description="Mechanic not found")

    if mechanic in ticket.mechanics:
        ticket.mechanics.remove(mechanic)
        db.session.commit()

    return ticket_schema.jsonify(ticket), 200

@service_ticket_bp.put("/<int:ticket_id>/add-part/<int:inventory_id>")
def add_part_to_ticket(ticket_id, inventory_id):
    ticket = db.session.get(ServiceTickets, ticket_id)
    if not ticket:
        abort(404, description="Service ticket not found")

    item = db.session.get(Inventory, inventory_id)
    if not item:
        abort(404, description="Inventory item not found")

    new_part = Part(inventory_id=inventory_id, service_ticket=ticket)
    db.session.add(new_part)

    db.session.commit()
    return {
        "message": f"Added 1 '{item.name}' to ticket {ticket_id}",
        "part_instance_id": new_part.id
    }, 200
    