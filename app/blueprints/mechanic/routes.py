from flask import request, jsonify, abort, g
from sqlalchemy import select, func, desc
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import db, Mechanic, TicketMechanics
from app.auth import encode_token, token_required
from . import mechanic_bp
from .schemas import MechanicSchema, LoginSchema
from app.blueprints.service_ticket.schemas import ServiceTicketSchema
from app.extensions import limiter, cache

mechanic_schema = MechanicSchema()
mechanics_schema = MechanicSchema(many=True)
login_schema = LoginSchema()
ticket_schema = ServiceTicketSchema(many=True)


@mechanic_bp.post("/")
def create_mechanic():
    data = request.get_json() or {}
    mechanic = mechanic_schema.load(data)

    mechanic.password = generate_password_hash(data["password"])

    db.session.add(mechanic)
    db.session.commit()
    return mechanic_schema.jsonify(mechanic), 201


@mechanic_bp.post("/login")
@limiter.limit("5 per minute")
def login():
    data = request.get_json() or {}
    creds = login_schema.load(data)

    email = creds["email"].strip().lower()
    password = creds["password"]

    mechanic = db.session.scalar(select(Mechanic).where(Mechanic.email == email))
    if not mechanic or not check_password_hash(mechanic.password, password):
        return jsonify({"error": "Invalid email or password"}), 401

    token = encode_token(mechanic.id)
    return jsonify({"token": token, "mechanic_id": mechanic.id}), 200


@mechanic_bp.get("/")
@cache.cached(timeout=60)
def get_mechanics():
    mechanics = db.session.scalars(select(Mechanic)).all()
    return mechanics_schema.jsonify(mechanics), 200


@mechanic_bp.get("/my-tickets")
@token_required
def my_tickets():
    mechanic_id = g.mechanic_id

    mechanic = db.session.get(Mechanic, mechanic_id)
    if not mechanic:
        abort(404, description="Mechanic not found")

    return ticket_schema.jsonify(mechanic.service_tickets), 200


@mechanic_bp.put("/<int:id>")
@token_required
def update_mechanic(id):
    mechanic_id = g.mechanic_id 

    if mechanic_id != id:
        return jsonify({"error": "Forbidden"}), 403

    mechanic = db.session.get(Mechanic, id)
    if not mechanic:
        abort(404, description="Mechanic not found")

    data = request.get_json() or {}

    if "password" in data:
        mechanic.password = generate_password_hash(data["password"])
        data.pop("password")

    allowed = {"first_name", "last_name", "email", "address", "salary"}
    for key, value in data.items():
        if key in allowed:
            setattr(mechanic, key, value)

    db.session.commit()
    return mechanic_schema.jsonify(mechanic), 200


@mechanic_bp.delete("/<int:id>")
@token_required
def delete_mechanic(id):
    mechanic_id = g.mechanic_id 

    if mechanic_id != id:
        return jsonify({"error": "Forbidden"}), 403

    mechanic = db.session.get(Mechanic, id)
    if not mechanic:
        abort(404, description="Mechanic not found")

    db.session.delete(mechanic)
    db.session.commit()
    return jsonify({"message": f"Mechanic {id} successfully deleted"}), 200

@mechanic_bp.get("/most-tickets")
def mechanics_by_most_tickets():
    statement = (
        select(
            Mechanic,
            func.count(TicketMechanics.ticket_id).label("ticket_count")
        )
        .join(TicketMechanics, TicketMechanics.mechanic_id == Mechanic.id, isouter=True)
        .group_by(Mechanic.id)
        .order_by(desc("ticket_count"))
    )
    rows = db.session.execute(statement).all()
    results = []
    for mechanic, ticket_count in rows:
        m = mechanic_schema.dump(mechanic)
        m["ticket_count"] = int(ticket_count or 0)
        results.append(m)

    return results, 200