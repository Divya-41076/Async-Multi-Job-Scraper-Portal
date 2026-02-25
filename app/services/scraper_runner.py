import time
import logging
from typing import Optional
from flask import current_app

from app.extensions.db import db # sql session
from app.models.job import Job #orm model
from app.services.status_store import status_store #progess tracking and polling


# this will runs in a bg thread
# updates in-memory runtime state(statusstore)
# persists durable dat to db
# doesnt talk to http or request objs

"""saves and converts the raw scraped data to job orm object and adds it to the sqlalchemy session"""

def _save_job(
        scrape_id: str,
        source: str,
        title:str,
        company:str,
        skills: str | None = None,
        experience: str | None = None,
        salary: str | None = None,
        location: str | None = None,):
    
    job = Job(
        scrape_id =scrape_id,
        source = source,
        title = title,
        company = company,
        skills = skills,
        experience = experience,
        salary = salary,
        location = location,
    )
    
    db.session.add(job)

def run_scrape_job(scrape_id: str, keyword:str):
    """ background task job runner and persists jobs to DB and updates in memory status."""

    try:
        status_store.start(scrape_id)
        
        status_store.increment_matched(scrape_id)

        with current_app.app_context():

            # internshala is the simulated version down below
            status_store.update_message(scrape_id, "scraping internshala")
            time.sleep(2)

            _save_job(
                scrape_id, source = "Internshala",
                title = "python developer intern",
                company = "ABC",
                skills = "python, flask",
                experience = "1-3 years",
                location = "remote",

            )
            status_store.increment_matched(scrape_id, 1)

            # timesjobs is the simulated version down below
            status_store.update_message(scrape_id, "scraping timesjobs")
            time.sleep(2)

            _save_job(
                scrape_id, source = "TimesJobs",
                title = "python developer intern",
                company = "ABC",
                skills = "python, flask",
                experience = "1-3 years",
                location = "remote",

            )
            status_store.increment_matched(scrape_id, 1)

            
            status_store.update_message(scrape_id, "scraping Bigshyft")
            time.sleep(2)

            _save_job(
                scrape_id, source = "Bigshyft",
                title = "python developer intern",
                company = "ABC",
                skills = "python, flask",
                experience = "1-3 years",
                location = "remote",

            )
            status_store.increment_matched(scrape_id, 1)
            
            # commit once (important)
            db.session.commit()

        status_store.complete(scrape_id)

    except Exception as e:
        db.session.rollback()
        status_store.fail(scrape_id,str(e))
            

# this is the main entry point for the bg thread to run the scrape job, it will be called from the api route handler
# it will run the scrape job and update the status store with the progress and results, it will also handle any exceptions that may occur during the scrape job and update the status store accordingly.
# the actual scraping logic is not implemented here, instead we are simulating the scraping process with time.sleep and hardcoded job data. the real implementation would involve making http requests to the target websites, parsing the html responses, extracting the relevant data, and then saving it to the database using the _save_job function.
# the status store is used to track the progress of the scrape job and to provide feedback to the client about the current status of the job. it allows us to update the message and the count of matched jobs as we go through the scraping process, and to mark the job as complete or failed at the end.
# the db.session.commit() is called once at the end of the scraping process to persist all the changes to the database in one transaction, which is more efficient than committing after each job is added. if any exception occurs during the scraping process, we rollback the session to avoid partial commits and mark the job as failed in the status store with the error message.
# this function is designed to be run in a background thread, so it does not interact with any request or http objects, and it uses the current_app context to access the database session and the status store.
# the _save_job function is a helper function that takes the raw scraped data and converts it into a Job ORM object, which is then added to the SQLAlchemy session. it does not commit the session, as the commit is handled in the main run_scrape_job function after all jobs have been added.
