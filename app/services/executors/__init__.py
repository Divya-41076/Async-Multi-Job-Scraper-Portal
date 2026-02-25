import os
from app.services.executors.thread_executor import ThreadExecutor

EXECUTOR_TYPE  = os.getenv("EXECUTOR_TYPE","thread")

def get_executor():
    #Future enhancements can be made here to add more executors like process based etc
    if EXECUTOR_TYPE == "thread":
        return ThreadExecutor()
    else:
        raise ValueError(f"Unknown EXECUTOR_TYPE: {EXECUTOR_TYPE}")

