from flask import request, abort
from sqlalchemy import select
from app.models import db, Customers
from . import customers_bp
from .schemas import customer_schema, customers_schema

@customers_bp.post("/")
def create_customer():
    data = request.get_json() or {}
    customer = customer_schema.load(data)
    db.session.add(customer)
    db.session.commit()
    return customer_schema.jsonify(customer), 201

@customers_bp.get("/")
def get_customers():
    email = request.args.get("email")
    page = request.args.get("page", default=1, type=int)
    per_page = request.args.get("per_page", default=10, type=int)

    if page < 1:
        page = 1
    if per_page < 1:
        per_page = 10
    if per_page > 50:
        per_page = 50

    if email:
        statement = select(Customers).where(Customers.email == email.strip().lower())
        customer = db.session.scalar(statement)
        if not customer:
            return {"error": "Customer not found"}, 404
        return customer_schema.jsonify(customer), 200

    statement = select(Customers).order_by(Customers.id)
    all_customers = db.session.scalars(statement).all()

    total = len(all_customers)
    start = (page - 1) * per_page
    end = start + per_page
    results = all_customers[start:end]
    return {
        "page": page,
        "per_page": per_page,
        "total": total,
        "results": customers_schema.dump(results),
    }, 200


@customers_bp.get("/<int:id>")
def get_customer(id):
    customer = db.session.get(Customers, id)
    if not customer:
        abort(404, description="Customer not found")
    return customer_schema.jsonify(customer), 200

@customers_bp.put("/<int:id>")
def update_customer(id):
    customer = db.session.get(Customers, id)
    if not customer:
        abort(404, description="Customer not found")

    data = request.get_json() or {}
    for key, value in data.items():
        if hasattr(customer, key):
            setattr(customer, key, value)

    db.session.commit()
    return customer_schema.jsonify(customer), 200

@customers_bp.delete("/<int:id>")
def delete_customer(id):
    customer = db.session.get(Customers, id)
    if not customer:
        abort(404, description="Customer not found")

    db.session.delete(customer)
    db.session.commit()
    return {"message": f"Customer {id} deleted"}, 200