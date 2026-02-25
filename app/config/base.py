import os

class BaseConfig:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")

    SQLALCHEMY_TRACK_MODIFICATIONS = False