import time
import requests
import logging
from flask import current_app

logger = logging.getLogger(__name__)

MAX_RETRIES = 3
TIMEOUT = 10
RESULTS_PER_PAGE = 50
PAGES = 2


def scrape(keyword: str, scrape_id: str, save_job_fn):
    """
    Fetches jobs from Adzuna API (India)
    returns metrics dict
    """
    metrics = {
        "total_fetched": 0,
        "matched": 0,
        "duplicates_skipped": 0,
        "success": True,
    }

    app_id = current_app.config.get("ADZUNA_APP_ID")
    app_key = current_app.config.get("ADZUNA_APP_KEY")

    if not app_id or not app_key:
        logger.error("Adzuna API keys missing in config")
        metrics["success"] = False
        return metrics

    for page in range(1, PAGES + 1):
        response = None
        for attempt in range(MAX_RETRIES):
            try:
                response = requests.get(
                    f"https://api.adzuna.com/v1/api/jobs/in/search/{page}",
                    params={
                        "app_id": app_id,
                        "app_key": app_key,
                        "results_per_page": RESULTS_PER_PAGE,
                        "what": keyword,
                        "content-type": "application/json",
                    },
                    timeout=TIMEOUT,
                )
                response.raise_for_status()
                break
            except Exception as e:
                logger.warning(f"Adzuna page {page} attempt {attempt+1} failed: {e}")
                if attempt == MAX_RETRIES - 1:
                    logger.error(f"Adzuna page {page} all retries failed")
                    metrics["success"] = False
                    return metrics

        jobs = response.json().get("results", [])
        metrics["total_fetched"] += len(jobs)

        for job in jobs:
            job_title = job.get("title", "")
            company = job.get("company", {}).get("display_name", "")
            location = job.get("location", {}).get("display_name", "")
            job_url = job.get("redirect_url", None)
            experience = job.get("contract_time", "Not specified")
            salary = str(job.get("salary_min", "Not disclosed"))

            saved = save_job_fn(
                scrape_id=scrape_id,
                source="Adzuna",
                title=job_title[:150],
                company=company[:120],
                skills=None,  # description is junk — cleaner to leave null
                experience=experience[:50],
                salary=salary[:50],
                location=location[:120],
                job_url=job_url[:500] if job_url else None,
            )

            if saved == "duplicate":
                metrics["duplicates_skipped"] += 1
            else:
                metrics["matched"] += 1
                logger.info(f"Saved Adzuna job: {job_title}")

            time.sleep(0.2)  # rate limiting

    logger.info(
        f"Adzuna done — fetched: {metrics['total_fetched']}, saved: {metrics['matched']}, duplicates: {metrics['duplicates_skipped']}"
    )
    return metrics
