from threading import Lock


class EngineManager:
    """Create the vLLM engines once, after the worker has accepted a job."""

    def __init__(self, factory):
        self._factory = factory
        self._lock = Lock()
        self._engines = None

    def get(self):
        if self._engines is None:
            with self._lock:
                if self._engines is None:
                    self._engines = self._factory()
        return self._engines

    @property
    def max_concurrency(self):
        if self._engines is None:
            return 1
        return self._engines[0].max_concurrency
