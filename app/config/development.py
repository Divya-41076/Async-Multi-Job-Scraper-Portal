import os
from .base import BaseConfig

class DevelopmentConfig(BaseConfig):
    DEBUG = True

    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_NAME = os.getenv("DB_NAME", "job_scraper")

    SQLALCHEMY_DATABASE_URI = (
        f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    )

    JOB_CLEANUP_AGE_SECONDS = int(os.getenv("JOB_CLEANUP_AGE_SECONDS", 21600)) # default 6 hours
    JOB_CLEANUP_INTERVAL_SECONDS = int(os.getenv("JOB_CLEANUP_INTERVAL_SECONDS", 300)) # default 5 minutes
    #     cleanup_age_seconds=app.config["JOB_CLEANUP_AGE_SECONDS"],
    # cleanup_interval_seconds=app.config["JOB_CLEANUP_INTERVAL_SECONDS"]