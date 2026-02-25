# app/api/jobs/routes.py
# this file contains the routes for job-related API endpoints
# it is mainly responsible for handling job data retrieval and management

from flask import Blueprint,request,jsonify
from sqlalchemy import desc,or_ # for ordering query results

from app.extensions.db import db
from app.models.job import Job

jobs_bp = Blueprint("jobs",__name__)


@jobs_bp.route("/jobs", methods=["GET"])
def list_jobs():
    """
    Docstring for list_jobs
    query params: this means extra data attached to the url to tell the server how you want the response like a filter opions or instructions sent along with the request
    https://example.com/search?key=value
    ? → starts query parameters
    key=value → one query parameter
    & → separates multiple query parameters

    keyword
    source
    location
    page(default=1)
    limit(default=20, max = 100)

    """

    keyword = request.args.get("keyword")
    source = request.args.get("source")
    location = request.args.get("location")

    page = int(request.args.get("page",1))
    limit = min(int(request.args.get("limit",20)),100)


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
    

    # Pagination
    total = query.count()

    jobs = (query
            .order_by(desc(Job.created_at))  #sorting with create_at and desc means descending order so the most recent jobs will be listed first
            .offset((page-1)*limit)
            .limit(limit).all())
    
    return jsonify({
        "page": page,
        "limit": limit,
        "total": total,
        # above is meta data and below is actual data
        "results": [job.to_dict() for job in jobs]
    }), 200