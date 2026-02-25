from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
load_dotenv()
import os

from app.config import config_by_name
from app.extensions.db import db
from app.api.health.routes import health_bp
from app.api.scrape.routes import scrape_bp
from app.api.jobs.routes import jobs_bp
from app.api.stats.routes import stats_bp
from app.services.status_store import StatusStore

def create_app():
    # load_dotenv()

    app = Flask(__name__)
    CORS(app)

    # Load config based on environment
    env = os.getenv("FLASK_ENV", "development")

    app.config.from_object(config_by_name[env])

    # Initialize extensions
    db.init_app(app)

    app.status_store = StatusStore(
    cleanup_age_seconds=app.config["JOB_CLEANUP_AGE_SECONDS"],
    cleanup_interval_seconds=app.config["JOB_CLEANUP_INTERVAL_SECONDS"]
    )

    # Register blueprints
    app.register_blueprint(health_bp)
    app.register_blueprint(scrape_bp)
    app.register_blueprint(jobs_bp)
    app.register_blueprint(stats_bp)

    return app