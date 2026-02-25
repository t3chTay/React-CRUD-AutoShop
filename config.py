class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI = "sqlite:///auto_shop.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "auto-shop-secret-123"
    DEBUG = True
    
    CACHE_TYPE = "SimpleCache"
    CACHE_DEFAULT_TIMEOUT = 60
    
class ProductionConfig:
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get("SECRET_KEY")
    DEBUG = False

    CACHE_TYPE = "SimpleCache"
    CACHE_DEFAULT_TIMEOUT = 60    