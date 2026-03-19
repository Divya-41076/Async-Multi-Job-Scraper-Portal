import logging
from flask import current_app

from app.extensions.db import db
from app.models.job import Job
from app.scrapers import scrape_remotive, scrape_jobicy, scrape_adzuna
from app.utils.db_retry import safe_db_write

logger = logging.getLogger(__name__)


def _save_job(
    scrape_id: str,
    source: str,
    title: str,
    company: str,
    skills: str | None = None,
    experience: str | None = None,
    salary: str | None = None,
    location: str | None = None,
    job_url: str | None = None,
):

    job = Job(
        scrape_id=scrape_id,
        source=source,
        title=title,
        company=company,
        skills=skills,
        experience=experience,
        salary=salary,
        location=location,
        job_url=job_url,
    )

    success = safe_db_write(operation=lambda: db.session.add(job), session=db.session)

    if not success:
        logger.info(f"Skipped job: {job_url}")
        return "duplicate"
    return "saved"


def _run_source(store, scrape_id, name, scrape_fn, keyword, save_fn):
    """
    Runs a single source scrape with its own commit.
    If it fails, logs warning and continues — other sources are unaffected.
    """
    try:
        store.update_message(scrape_id, f"scraping {name}")
        metrics = scrape_fn(keyword, scrape_id, save_fn)
        db.session.commit()  # commit after each source
        store.increment_matched(scrape_id, metrics["matched"])
        logger.info(
            f"{name} — fetched: {metrics['total_fetched']}, "
            f"saved: {metrics['matched']}, "
            f"duplicates: {metrics['duplicates_skipped']}, "
            f"success: {metrics['success']}"
        )
    except Exception as e:
        db.session.rollback()
        logger.warning(f"{name} source failed: {e} — continuing with other sources")


def run_scrape_job(app, scrape_id: str, keyword: str):
    """background task — runs all scrapers, persists to DB, updates in-memory status."""

    try:
        with app.app_context():
            store = current_app.status_store
            store.start(scrape_id)

            _run_source(
                store, scrape_id, "Remotive", scrape_remotive, keyword, _save_job
            )
            _run_source(store, scrape_id, "Jobicy", scrape_jobicy, keyword, _save_job)
            _run_source(store, scrape_id, "Adzuna", scrape_adzuna, keyword, _save_job)

            store.complete(scrape_id)

    except Exception as e:
        logger.exception("Scrape job %s failed: %s", scrape_id, e)
        try:
            with app.app_context():
                db.session.rollback()
                current_app.status_store.fail(scrape_id, str(e))
        except Exception:
            pass


"""
```

---

**New folder structure:**
```
app/
└── utils/
    ├── __init__.py  ← empty
    └── db_retry.py

"""


# this is the main entry point for the bg thread to run the scrape job, it will be called from the api route handler
# it will run the scrape job and update the status store with the progress and results, it will also handle any exceptions that may occur during the scrape job and update the status store accordingly.
# the actual scraping logic is not implemented here, instead we are simulating the scraping process with time.sleep and hardcoded job data. the real implementation would involve making http requests to the target websites, parsing the html responses, extracting the relevant data, and then saving it to the database using the _save_job function.
# the status store is used to track the progress of the scrape job and to provide feedback to the client about the current status of the job. it allows us to update the message and the count of matched jobs as we go through the scraping process, and to mark the job as complete or failed at the end.
# the db.session.commit() is called once at the end of the scraping process to persist all the changes to the database in one transaction, which is more efficient than committing after each job is added. if any exception occurs during the scraping process, we rollback the session to avoid partial commits and mark the job as failed in the status store with the error message.
# this function is designed to be run in a background thread, so it does not interact with any request or http objects, and it uses the current_app context to access the database session and the status store.
# the _save_job function is a helper function that takes the raw scraped data and converts it into a Job ORM object, which is then added to the SQLAlchemy session. it does not commit the session, as the commit is handled in the main run_scrape_job function after all jobs have been added.
