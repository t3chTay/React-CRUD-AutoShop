import jwt
from datetime import datetime, timedelta, timezone
from functools import wraps
from flask import current_app, request, jsonify, g

def encode_token(mechanic_id: int) -> str:
    secret = current_app.config.get("SECRET_KEY")
    if not secret:
        raise RuntimeError("SECRET_KEY is not set in app config")

    payload = {
        "sub": str(mechanic_id),
        "iat": datetime.now(timezone.utc),
        "exp": datetime.now(timezone.utc) + timedelta(hours=24),
    }
    return jwt.encode(payload, secret, algorithm="HS256")

def decode_token(token: str) -> int:
    secret = current_app.config.get("SECRET_KEY")
    if not secret:
        raise RuntimeError("SECRET_KEY is not set in app config")

    payload = jwt.decode(token, secret, algorithms=["HS256"])
    return int(payload["sub"])

def token_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        auth = request.headers.get("Authorization", "")

        parts = auth.split()

        if len(parts) != 2 or parts[0].lower() != "bearer":
            return jsonify({
                "error": "Missing or invalid Authorization header",
                "hint": "Use: Authorization: Bearer <token>"
            }), 401

        token = parts[1].strip()

        try:
            mechanic_id = decode_token(token)
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expired"}), 401
        except jwt.InvalidTokenError as e:
            return jsonify({"error": "Invalid token", "detail": str(e)}), 401

        g.mechanic_id = mechanic_id
        return f(*args, **kwargs)

    return wrapper