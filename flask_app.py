from app import create_app
from app.models import db

app = create_app("ProductionConfig")
