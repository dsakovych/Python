class ThreadWithReturn(Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None):
        super(self.__class__, self).__init__(group, target, name, args, kwargs)
        self._return = None

    def run(self):
        if self._target:
            self._return = self._target(*self._args, **self._kwargs)

    def join(self, timeout=None):
        Thread.join(self)
        return self._return
