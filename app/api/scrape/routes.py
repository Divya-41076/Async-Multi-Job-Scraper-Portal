import uuid
import datetime
from flask import Blueprint,request,jsonify,current_app

# from app.services.status_store import status_store

from app.services.executors import get_executor
from app.services.scraper_runner import run_scrape_job


scrape_bp = Blueprint("scrape",__name__)
executor = get_executor()


@scrape_bp.route("/scrape",methods=["POST"])
def start_scrape():
    data = request.get_json(silent=True) or {}
    keyword = data.get("keyword")

    # genrate scrape_id
    scrape_id = str(uuid.uuid4())

    # create a scrapejob in status store
    current_app.status_store.create(scrape_id=scrape_id,keyword = keyword)

    # start the async scrape job  your bankground taks starts...
    executor.submit(run_scrape_job,current_app._get_current_object(),scrape_id,keyword)

    # return immediately(async willl be added later)
    return jsonify({
        "scrape_id":scrape_id,
        "status":"PENDING",
        "message":"Scrape job created"
    }),202  
# 202 Accepted 

@scrape_bp.route("/scrape/status/<scrape_id>", methods=["GET"])
def get_scrape_status(scrape_id:str):
    job = current_app.status_store.get(scrape_id) #get job from status store

    if not job:
        return jsonify({
            "error": "Invalid scrape_id",
            "message": "No scrape job found for this id"
        }),404
# 404 Not Found

    return jsonify({
        "scrape_id": job["scrape_id"],
        "keyword": job["keyword"],
        "state": job["state"],
        "message":job["message"],
        "matched": job["matched"],
        "started_at": datetime.datetime.fromtimestamp(job["started_at"]).isoformat() if job["started_at"] else None,
        "finished_at": datetime.datetime.fromtimestamp(job["finished_at"]).isoformat() if job["finished_at"] else None,
        "error": job["error"]
    }), 200