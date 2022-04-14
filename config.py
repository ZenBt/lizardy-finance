import decouple

class Configuration:
    SECRET_KEY = decouple.config('SECRET_KEY')
    DEBUG = decouple.config('DEBUG')
    SQLALCHEMY_DATABASE_URI = decouple.config('SQLALCHEMY_DATABASE_URI')
