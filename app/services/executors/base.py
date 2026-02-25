class BaseExecutor:
    def submit(self,fn,*args,**kwargs):
        raise NotImplementedError("Submit method must be implemented by subclasses")
    # above means any subclass of BaseExecutor must implement submit method