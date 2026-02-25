import os
import threading
import time
from enum import Enum
from typing import Dict,Any,Optional,List


class ScrapeState(str,Enum):
    PENDING ="PENDING"
    RUNNING ="RUNNING"
    COMPLETED = 'COMPLETED'
    FAILED = 'FAILED'
    CANCELLED = 'CANCELLED'
    TIMEOUT = 'TIMEOUT'
    ABORTED = 'ABORTED'


VALID_TRANSITIONS ={
    ScrapeState.PENDING: {ScrapeState.RUNNING, ScrapeState.FAILED},
    ScrapeState.RUNNING: {ScrapeState.COMPLETED, ScrapeState.FAILED},
}

class StatusStore:
    def __init__(self, cleanup_age_seconds:int | None =None,cleanup_interval_seconds: int | None = None):
        self._lock = threading.Lock()
        self._store: Dict[str,Dict[str,Any]] ={}   #_store = {"scrape_id":{"scrape_data": none}}

        self._cleanup_age = cleanup_age_seconds or int(os.getenv("JOB_CLEANUP_AGE_SECONDS", 21600)) # default 6 hours
        self._cleanup_interval = cleanup_interval_seconds or int(os.getenv("JOB_CLEANUP_INTERVAL_SECONDS", 300)) # default 5 minutes
       
        # start cleanup thread only if enabled
        if self._cleanup_age>0 and self._cleanup_interval > 0:
            self._start_cleanup_worker()

# internal
    def _can_transition(self, current_state: ScrapeState, target: ScrapeState) -> bool:
        allowed_states = VALID_TRANSITIONS.get(current_state, set())
        return target in allowed_states
    
    def _start_cleanup_worker(self) -> None:
        def cleanup_worker():
            while True:
                time.sleep(self._cleanup_interval)
                self._cleanup_old_jobs()
        thread = threading.Thread(
            target = cleanup_worker,
            daemon=True
        )
        thread.start()

# cleanup
    def _cleanup_old_jobs(self) -> None:
        # remove completed or failed jobs older than cleanup age.
        # returns number of jobs removed

        with self._lock:
            now = time.time()
            to_remove =[
                scrape_id for scrape_id, job in self._store.items()
                if job["finished_at"] and (now-job["finished_at"]) > self._cleanup_age]
            
            for scrape_id in to_remove:
                del self._store[scrape_id]

            return len(to_remove)

# create
    def create(self, scrape_id:str, keyword:Optional[str] =None) -> None:
        with self._lock:
            self._store[scrape_id] = {
                "scrape_id":scrape_id,
                "keyword": keyword,#for eg 'python developer'
                "state": ScrapeState.PENDING,
                "message":"Queued",
                "matched":0, #initially is zero
                "started_at": None,
                "finished_at": None,
                "error":None
            }
# state management
# now the life cycle methods for scrape jobs

    def start(self, scrape_id:str)->None:
        """Mark scrape job as running"""
        with self._lock:
            job = self._store.get(scrape_id)
            if not job:
                return
            
            if not self._can_transition(job["state"], ScrapeState.RUNNING):
                return # invalid transition
            
            job["started_at"] = time.time()
            job["state"] = ScrapeState.RUNNING
            job["message"] = "Scraping started"


        # completed is a terminal state
    def complete(self, scrape_id:str, message:str="Scraping Completed")->None:
        """Mark scrape job as completed"""
        with self._lock:
            job = self._store.get(scrape_id)
            if not job:
                return 
            
            if not self._can_transition(job["state"], ScrapeState.COMPLETED):
                return # invalid transition

            job["state"] = ScrapeState.COMPLETED #enUM VALUE
            job["message"] = "Scraping completed"
            job["finished_at"] = time.time()

        # failed is a terminal state
    def fail(self, scrape_id:str, error: Optional[str] =None) ->None:
        """Mark scrape job as failed"""
        with self._lock:
            job = self._store.get(scrape_id)
            if not job:
                return 
            
            if not self._can_transition(job["state"], ScrapeState.FAILED):
                return

            job["state"] = ScrapeState.FAILED
            job["error"] = error
            job["message"] = "Scraping failed"
            job["finished_at"] = time.time()


# update state and update message and increment methods are helper methods - that is to assist and not finalize
    def update_state(self, scrape_id:str, state: ScrapeState)->None:
        with self._lock:
            job = self._store.get(scrape_id)
            if not job:
                return
            
            if not self._can_transition(job["state"], state):
                return

            
            job["state"] = state


    def update_message(self,scrape_id:str,message:str)->None:
        with self._lock:
            job = self._store.get(scrape_id)
            if job:
                job["message"] = message


    def increment_matched(self, scrape_id:str, count:int =1)->None:
        with self._lock:
            job = self._store.get(scrape_id)
            if job:
                job["matched"] += count

# read
    def get(self, scrape_id:str) -> Optional[Dict[str,Any]]:
        with self._lock:
            job = self._store.get(scrape_id)
            return dict(job) if job else None
    
    def all(self) -> List[Dict[str,Any]]:
        # return all scrape jobs as copies
        with self._lock:
            return[dict(job) for job in self._store.values()]
        
# delete
    def delete(self,scrape_id:str) ->None:
        with self._lock:
            self._store.pop(scrape_id, None)


status_store = StatusStore()