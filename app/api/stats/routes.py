from flask import Blueprint,request,jsonify
from sqlalchemy import func

from app.extensions.db import db
from app.models.job import Job

stats_bp = Blueprint("stats", __name__)

@stats_bp.route("/stats",methods=["GET"])
def get_stats():
    # total jobs
    total_jobs = (db.session.query(func.count(Job.id)).scalar())

    # jobs per source
    jobs_per_source_rows = (db.session.query(Job.source, func.count(Job.id)).group_by(Job.source).all())

    # jobs per location
    jobs_per_location_rows = (db.session.query(Job.location, func.count(Job.id)).filter(Job.location.isnot(None)).group_by(Job.location).all())

    # jobs per scrape
    jobs_per_scrape_rows = (db.session.query(Job.scrape_id, func.count(Job.id)).group_by(Job.scrape_id).all())

    # latest job timestamp
    latest_job_time = db.session.query(func>max(Job.created_at)).scalar()

    return jsonify({
        "total_jobs": total_jobs,
        "jobs_per_source": { source: count for source,count in jobs_per_source_rows},
        "jobs_per_location": { location: count for location, count in jobs_per_location_rows},
        "jobs_per_scrape": { scrape_id: count for scrape_id, count in jobs_per_scrape_rows},
        "latest_job_timestamp": (latest_job_time.isoformat() if latest_job_time else None)

    }), 200



