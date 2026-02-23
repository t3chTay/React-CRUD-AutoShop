from flask import request, jsonify, abort
from sqlalchemy import select
from app.models import db, Mechanic
from . import mechanic_bp
from .schemas import MechanicSchema

mechanic_schema = MechanicSchema()
mechanics_schema = MechanicSchema(many=True)

@mechanic_bp.post("/")
def create_mechanic():
    data = request.get_json() or {}
    mechanic = mechanic_schema.load(data)
    db.session.add(mechanic)
    db.session.commit()
    return mechanic_schema.jsonify(mechanic), 201

@mechanic_bp.get("/")
def get_mechanics():
    mechanics = db.session.scalars(select(Mechanic)).all()
    return mechanics_schema.jsonify(mechanics), 200

@mechanic_bp.put("/<int:id>")
def update_mechanic(id):
    mechanic = db.session.get(Mechanic, id)
    if not mechanic:
        abort(404, description="Mechanic not found")

    data = request.get_json() or {}
    for key, value in data.items():
        if hasattr(mechanic, key):
            setattr(mechanic, key, value)

    db.session.commit()
    return mechanic_schema.jsonify(mechanic), 200

@mechanic_bp.delete("/<int:id>")
def delete_mechanic(id):
    mechanic = db.session.get(Mechanic, id)
    if not mechanic:
        abort(404, description="Mechanic not found")

    db.session.delete(mechanic)
    db.session.commit()
    return jsonify({"message": f"Mechanic {id} successfully deleted"}), 200