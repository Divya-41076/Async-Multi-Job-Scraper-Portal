import logging
from datetime import datetime, timedelta
from sqlalchemy import desc, or_

from app.extensions import db
from app.models.job import Job

logger = logging.getLogger(__name__)

STALE_THRESHOLD_HOURS = 1

def is_stale(keyword:str = None)-> bool:
    """
    checks if the job data is stale or empty
    if keyword provided - check staleness
    if no keyword check overall latest job.
    """
    try:
        query = Job.query

        if keyword:
            query = query.filter(
                or_(
                    Job.title.ilike(f"%{keyword}%"),
                    Job.skills.ilike(f"%{keyword}%")
                )
            )

        latest_job = query.order_by(desc(Job.created_at)).first()
        logger.info(f"Latest job time: {latest_job.created_at}")
        
        if not latest_job:
            logger.info(f"No jobs found for keyword'{keyword}' - stale")
            return True
        
        # check if latest job is older than threshold
        age = datetime.utcnow() - latest_job.created_at
        stale = age > timedelta(hours = STALE_THRESHOLD_HOURS)

        if stale:
            logger.info(f"Data is stale for keyword '{keyword}' - age: {age}")

        return stale
    except Exception as e:
        logger.error(f"is_stale check failed:{e}")
        return False
    # if check fails dont trigger the scrape - better to have old data than no data