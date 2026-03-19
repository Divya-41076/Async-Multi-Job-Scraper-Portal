# app/api/jobs/routes.py
# this file contains the routes for job-related API endpoints
# it is mainly responsible for handling job data retrieval and management

from flask import Blueprint,request,jsonify, current_app
from sqlalchemy import desc,or_ # for ordering query results
import uuid

from app.extensions.db import db
from app.models.job import Job
from app.utils.freshness import is_stale
from app.services.scraper_runner import run_scrape_job
from app.services.executors import get_executor

import logging
logger = logging.getLogger(__name__)

jobs_bp = Blueprint("jobs",__name__)
executor = get_executor()

@jobs_bp.route("/jobs", methods=["GET"])
def list_jobs():
    """
    Docstring for list_jobs
    query params: this means extra data attached to the url to tell the server how you want the response like a filter opions or instructions sent along with the request
    https://example.com/search?key=value
    ? → starts query parameters
    key=value → one query parameter
    & → separates multiple query parameters

    keyword - search in title and skills
    source - filter by source
    location - filter by location
    page(default=1)
    limit(default=20, max = 100)
    sort - by latest

    """

    keyword = request.args.get("keyword")
    source = request.args.get("source")
    location = request.args.get("location")
    sort = request.args.get("sort")

    try:
        page = int(request.args.get("page",1))
        limit = min(int(request.args.get("limit",20)),100)
    except ValueError:
        return jsonify({
            "error":"invalid params",
            "message": "page and limit must be integers"
        }),400


    # base query
    query = Job.query

    # filters
    if keyword:  #if keyword is provided, filter jobs where title or skills contain the keyword (case-insensitive)
        query = query.filter(
            or_(Job.title.ilike(f"%{keyword}%"),
                Job.skills.ilike(f"%{keyword}%")))
        
    if source:
        query = query.filter(Job.source == source)
    
    if location:
        query = query.filter(Job.location.ilike(f"%{location}%"))
    
    # sorting
    if sort == "latest":
        query = query.order_by(desc(Job.created_at))

    # Pagination
    total = query.count()

    jobs = (query
            # .order_by(desc(Job.created_at))  #sorting with create_at and desc means descending order so the most recent jobs will be listed first
            .offset((page-1)*limit)
            .limit(limit)
            .all())
    
    # smart trigger
   # smart trigger — check if data is stale and no scrape is running
    scrape_triggered = False
    if keyword:
        stale = is_stale(keyword)  # store result — avoid double call
        if stale:
            store = current_app.status_store
            if not store.is_scrape_running(keyword):
                scrape_id = str(uuid.uuid4())
                store.create(scrape_id=scrape_id, keyword=keyword)
                try:
                    executor.submit(
                        run_scrape_job,
                        current_app._get_current_object(),
                        scrape_id,
                        keyword
                    )
                    scrape_triggered = True
                    logger.info(f"Triggering scrape for keyword={keyword}, scrape_id={scrape_id}")
                except Exception as e:
                    logger.error(f"Failed to submit scrape job: {e}")

    return jsonify({
        "page": page,
        "limit": limit,
        "total": total,
        "scrape_triggered": scrape_triggered, 
        # above is meta data and below is actual data
        "results": [job.to_dict() for job in jobs]
    }), 200