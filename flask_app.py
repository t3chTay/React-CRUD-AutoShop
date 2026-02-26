from app import create_app
from app.models import db

app = create_app("ProductionConfig")

@app.get("/init-db")
def init_db():
    db.create_all()
    return {"message": "DB initialized"}, 200