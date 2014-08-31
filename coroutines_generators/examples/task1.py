from concurrent.futures import ThreadPoolExecutor
import time

class Task:
    """Task class wraps around and represents a running generator."""

    def __init__(self, gen):
        """Initialize task object with generator."""
        self._gen = gen

    def step(self, value=None):
        """Advance the generator to the next yield, sending in a value."""
        try:
            fut = self._gen.send(value)
            # attach callback to the produced future
            fut.add_done_callback(self._wakeup)
        except StopIteration as exc:
            pass

    def _wakeup(self, fut):
        """Callback function called in response to receiving result."""
        result = fut.result()
        # this little trick will allow us to run to the next yield
        self.step(result)

def recursive(pool, n):
    """Recursive function, using yield statements."""
    yield pool.submit(time.sleep, 0.001)
    print(n)
    # let's call create another object of ourselves and run it
    # sort of recursion in a very weird way
    Task(recursive(pool, n+1)).step()


if __name__ == '__main__':
    # first we need to create pool executor
    pool = ThreadPoolExecutor(8)

    # now call our recursive function using the Task object
    Task(recursive(pool, 0)).step()

    # make sure we don't loose the input
    while True:
        pass

