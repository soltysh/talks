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

def run_future(gen):
    t = Task(gen)
    t.step()
    return t

def run_thread(gen):
    value = None
    while True:
        try:
            fut = gen.send(value)
            value = fut.result()
        except StopIteration as exc:
            return exc.value

def fib(n):
    return 1 if n <= 2 else (fib(n-1) + fib(n-2))

def do_fib(pool, n):
    result = []
    for i in range(n):
        val = yield from pool.submit(fib, i)
        result.append(val)
    return result

def do_fib2(pool, n):
    fut = pool.submit(fib, n)
    return fut.result()

if __name__ == '__main__':
    # first we need to create pool executor
    pool = ProcessPoolExecutor(8)

    # start = time.time()
    # t1 = run_future(do_fib(pool, 34))
    # t1.result()

    # t2 = run_future(do_fib(pool, 34))
    # t2.result()
    # end = time.time()
    # print("Sequential: ", (end - start))

    # to verify!!!
    start = time.time()
    tpool = ThreadPoolExecutor(8)
    t1 = tpool.submit(do_fib2, pool, 34)
    t2 = tpool.submit(do_fib2, pool, 34)
    print(t1.result())
    print(t2.result())
    end = time.time()
    print("Parallel: ", (end - start))
