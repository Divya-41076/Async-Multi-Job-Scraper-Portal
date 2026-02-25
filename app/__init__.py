from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

from app.extensions.db import db
from app.api.health.routes import health_bp
from app.api.scrape.routes import scrape_bp
from app.api.jobs.routes import jobs_bp
from app.api.stats.routes import stats_bp

load_dotenv()

def create_app():
    app =Flask(__name__)
    CORS(app)
    #load config(defualt:development)
    app.config.from_object("app.config.development.DevelopmentConfig")

    #initialize extensions
    db.init_app(app)

    # register the blueprints
    app.register_blueprint(health_bp)
    app.register_blueprint(scrape_bp)
    app.register_blueprint(jobs_bp)
    app.register_blueprint(stats_bp)


    return app