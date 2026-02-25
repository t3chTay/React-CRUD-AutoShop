import unittest
from app import create_app
from app.models import db, Mechanic
from werkzeug.security import generate_password_hash
from app.auth import encode_token


class MechanicTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app("DevelopmentConfig")
        self.app.config.update({
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:", # so i dont use my original database
            "RATELIMIT_ENABLED": False,
            "CACHE_TYPE": "NullCache"
        })
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
            db.engine.dispose()

    def create_mechanic(self):
        return self.client.post("/mechanics/", json={
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@test.com",
            "address": "123 street",
            "salary": 50000,
            "password": "password123"
        })

    def test_create_mechanic(self):
        response = self.create_mechanic()
        self.assertEqual(response.status_code, 201)

    def test_create_mechanic_missing_field(self):
        response = self.client.post("/mechanics/", json={
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@test.com",
            "salary": 50000
        })
        self.assertEqual(response.status_code, 400)

    def test_login(self):
        self.create_mechanic()
        response = self.client.post("/mechanics/login", json={
            "email": "john@test.com",
            "password": "password123"
        })
        self.assertEqual(response.status_code, 200)

    def test_login_invalid(self):
        self.create_mechanic()
        response = self.client.post("/mechanics/login", json={
            "email": "john@test.com",
            "password": "wrong"
        })
        self.assertEqual(response.status_code, 401)


    def test_get_mechanics(self):
        self.create_mechanic()
        response = self.client.get("/mechanics/")
        self.assertEqual(response.status_code, 200)

    def test_my_tickets_no_token(self):
        response = self.client.get("/mechanics/my-tickets")
        self.assertEqual(response.status_code, 401)

    def test_update_mechanic(self):
        self.create_mechanic()
        with self.app.app_context():
            mech = db.session.query(Mechanic).first()
            token = encode_token(mech.id)

        response = self.client.put(
            f"/mechanics/{mech.id}",
            headers={"Authorization": f"Bearer {token}"},
            json={"first_name": "Updated"}
        )
        self.assertEqual(response.status_code, 200)


    def test_update_forbidden(self):
        self.create_mechanic()
        with self.app.app_context():
            mech = db.session.query(Mechanic).first()
            token = encode_token(999)

        response = self.client.put(
            f"/mechanics/{mech.id}",
            headers={"Authorization": f"Bearer {token}"},
            json={"first_name": "Updated"}
        )
        self.assertEqual(response.status_code, 403)

    def test_delete_mechanic(self):
        self.create_mechanic()
        with self.app.app_context():
            mech = db.session.query(Mechanic).first()
            token = encode_token(mech.id)

        response = self.client.delete(
            f"/mechanics/{mech.id}",
            headers={"Authorization": f"Bearer {token}"}
        )
        self.assertEqual(response.status_code, 200)

    def test_delete_no_token(self):
        response = self.client.delete("/mechanics/1")
        self.assertEqual(response.status_code, 401)