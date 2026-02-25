from flask import request, abort
from sqlalchemy import select
from app.models import db, Inventory
from . import parts_bp
from .schemas import inventory_schema, inventories_schema

@parts_bp.post("/")
def create_inventory_item():
    data = request.get_json() or {}
    item = inventory_schema.load(data)
    db.session.add(item)
    db.session.commit()
    return inventory_schema.jsonify(item), 201

@parts_bp.get("/")
def get_inventory():
    items = db.session.scalars(select(Inventory)).all()
    return inventories_schema.jsonify(items), 200

@parts_bp.get("/<int:id>")
def get_inventory_item(id):
    item = db.session.get(Inventory, id)
    if not item:
        abort(404, description="Inventory item not found")
    return inventory_schema.jsonify(item), 200

@parts_bp.put("/<int:id>")
def update_inventory_item(id):
    item = db.session.get(Inventory, id)
    if not item:
        abort(404, description="Inventory item not found")

    data = request.get_json() or {}
    allowed = {"name", "price"}
    for k, v in data.items():
        if k in allowed:
            setattr(item, k, v)

    db.session.commit()
    return inventory_schema.jsonify(item), 200

@parts_bp.delete("/<int:id>")
def delete_inventory_item(id):
    item = db.session.get(Inventory, id)
    if not item:
        abort(404, description="Inventory item not found")

    db.session.delete(item)
    db.session.commit()
    return {"message": f"Inventory item {id} deleted"}, 200