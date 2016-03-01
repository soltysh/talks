from concurrent.futures import ThreadPoolExecutor, Future, ProcessPoolExecutor
import time


def patch_future(cls):
    """Patch Future object to be able to get the result of a Task."""
    def __iter__(self):
        if not self.done():
            yield self
        return self.result()
    cls.__iter__ = __iter__
patch_future(Future)

class Task(Future):
    """Task class wraps around and represents a running generator."""

    def __init__(self, gen):
        """Initialize task object with generator."""
        super().__init__()
        self._gen = gen

    def step(self, value=None):
        """Advance the generator to the next yield, sending in a value."""
        try:
            fut = self._gen.send(value)
            # attach callback to the produced future
            fut.add_done_callback(self._wakeup)
        except StopIteration as exc:
            # set the result of the task
            self.set_result(exc.value)

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
    result = yield from pool.submit(executor, x, y)
    return result


if __name__ == '__main__':
    # first we need to create pool executor
    pool = ProcessPoolExecutor(8)

    # run calculation and print the result
    t = Task(do_exec(pool, 2, 3))
    t.step()
    print("Got ", t.result())
