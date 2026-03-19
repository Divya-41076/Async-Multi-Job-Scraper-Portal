import time
import logging

from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

CLEANUP_INTERVAL_SECONDS = 86400 # default 1 hour
JOB_MAX_AGE_DAYS = 14

def start_cleanup_worker(app):
    """
    bg thread that deletes jobs older than 14 days.
    runs every day once independently
    """

    import threading

    def cleanup_worker():
        while True:
            try:
                with app.app_context():
                    from app.extensions import db
                    from app.models.job import Job

                    cutoff = datetime.utcnow() - timedelta(days = JOB_MAX_AGE_DAYS)

                    deleted = db.session.query(Job).filter(
                        Job.created_at < cutoff
                    ).delete()

                    db.session.commit()
                    logger.info(f"cleanup :deleted {deleted} old jobs")

            except Exception as e:
                logger.error(f"cleanup failed :{e}")

            time.sleep(CLEANUP_INTERVAL_SECONDS)

    thread = threading.Thread(target=cleanup_worker, daemon = True)
    thread.start()
    logger.info("cleanup worker started")


# it will cleanup first and then sleep for 24 hours. so if the app restarts it will cleanup immediately and then wait for next cycle.