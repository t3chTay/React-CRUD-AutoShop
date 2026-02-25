class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI = "sqlite:///auto_shop.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "auto-shop-secret-123"
    DEBUG = True
    
    CACHE_TYPE = "SimpleCache"
    CACHE_DEFAULT_TIMEOUT = 60