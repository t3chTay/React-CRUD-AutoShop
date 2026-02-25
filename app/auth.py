from jose import jwt, JWTError, ExpiredSignatureError
from datetime import datetime, timedelta, timezone
from functools import wraps
from flask import current_app, request, jsonify, g

ALGORITHM = "HS256"

def encode_token(mechanic_id: int) -> str:
    secret = current_app.config.get("SECRET_KEY")
    if not secret:
        raise RuntimeError("SECRET_KEY is not set")

    now = datetime.now(timezone.utc)
    payload = {
        "sub": str(mechanic_id),
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(hours=24)).timestamp()),
    }
    return jwt.encode(payload, secret, algorithm=ALGORITHM)

def decode_token(token: str) -> int:
    secret = current_app.config.get("SECRET_KEY")
    if not secret:
        raise RuntimeError("SECRET_KEY is not set")

    payload = jwt.decode(token, secret, algorithms=[ALGORITHM])
    return int(payload["sub"])

def token_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        auth = request.headers.get("Authorization", "")
        parts = auth.split()

        if len(parts) != 2 or parts[0].lower() != "bearer":
            return jsonify({
                "error": "Missing or invalid Authorization header. Use Bearer <token>"
            }), 401

        token = parts[1].strip()

        try:
            g.mechanic_id = decode_token(token)
        except ExpiredSignatureError:
            return jsonify({"error": "Token expired"}), 401
        except JWTError:
            return jsonify({"error": "Invalid token"}), 401

        return f(*args, **kwargs)
    return wrapper