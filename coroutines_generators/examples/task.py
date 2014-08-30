class Task:
    """Task class wraps around and represents a running generator."""

    def __init__(self, gen):
        """Initialize task object with generator."""
        self._gen = gen

    def step(self, value=None):
        """Proceed with execution to the next yield statement."""
        try:
            fut = self._gen.send(value)
            fut.add_done_callback(self._wakeup)
        except StopIteration as exc:
            pass

    def _wakeup(self, fut):
        """Callback function called in response to receiving result."""
        result = fut.result()
        self.step(result)
