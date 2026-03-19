import time
import requests
import logging

logger = logging.getLogger(__name__)

MAX_RETRIES = 3
TIMEOUT = 10


def scrape(keyword: str, scrape_id: str, save_job_fn):
    """
    Fetches jobs from Jobicy public API
    returns metrics dict
    """
    metrics = {
        "total_fetched": 0,
        "matched": 0,
        "duplicates_skipped": 0,
        "success": True,
    }

    response = None
    for attempt in range(MAX_RETRIES):
        try:
            response = requests.get(
                "https://jobicy.com/api/v2/remote-jobs",
                params={"count": 50, "tag": keyword},
                timeout=TIMEOUT,
            )
            response.raise_for_status()
            break
        except Exception as e:
            logger.warning(f"Jobicy attempt {attempt+1} failed: {e}")
            if attempt == MAX_RETRIES - 1:
                logger.error("Jobicy all retries failed")
                metrics["success"] = False
                return metrics

    jobs = response.json().get("jobs", [])
    metrics["total_fetched"] = len(jobs)

    for job in jobs:
        job_title = job.get("jobTitle", "")
        company = job.get("companyName", "")
        location = job.get("jobGeo", "Remote")
        job_url = job.get("url", None)
        skills = ", ".join(job.get("jobIndustry", []))
        experience = job.get("jobLevel", "Not specified")

        saved = save_job_fn(
            scrape_id=scrape_id,
            source="Jobicy",
            title=job_title[:150],
            company=company[:120],
            skills=skills[:500],
            experience=experience[:50],
            salary="Not disclosed",
            location=location[:120],
            job_url=job_url[:500] if job_url else None,
        )

        if saved == "duplicate":
            metrics["duplicates_skipped"] += 1
        else:
            metrics["matched"] += 1
            logger.info(f"Saved Jobicy job: {job_title}")

        time.sleep(0.2)  # rate limiting

    logger.info(
        f"Jobicy done — fetched: {metrics['total_fetched']}, saved: {metrics['matched']}, duplicates: {metrics['duplicates_skipped']}"
    )
    return metrics
