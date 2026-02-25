from flask_marshmallow import Marshmallow
from flask_limiter import Limiter
from flask import request
from flask_caching import Cache

ma = Marshmallow()
cache = Cache()
limiter = Limiter(
    key_func=lambda: request.remote_addr,
    default_limits=["400 per day", "100 per hour"]
)