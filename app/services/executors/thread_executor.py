import threading
from app.services.executors.base import BaseExecutor

class ThreadExecutor(BaseExecutor):
    def submit(self,fn,*args,**kwargs):
        thread = threading.Thread( 
            target=fn,
            args=args,
            kwargs=kwargs,
            daemon=True # daemon thread will not block program exit namely it will exit when main program exits and 
        )
        thread.start()
