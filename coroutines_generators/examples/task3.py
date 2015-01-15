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

def executor(x, y):
    """Very complex calculation."""
    print("I'm going to sleep for a while...")
    time.sleep(10)
    return x + y

def do_exec(pool, x, y):
    result = yield pool.submit(executor, x, y)
    print("Got: ", result)


if __name__ == '__main__':
    # first we need to create pool executor
    pool = ThreadPoolExecutor(8)

    # now call our recursive function using the Task object
    Task(do_exec(pool, 1, 2)).step()

    # make sure we don't loose the input
    while True:
        pass

