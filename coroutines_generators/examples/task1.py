from task import Task
from concurrent.futures import ThreadPoolExecutor
import time

def executor(x, y):
    """Execution of very complex task asynchronously"""
    print("I'm going to sleep for a while...")
    time.sleep(10)
    return x + y

def do_executor(pool, x, y):
    result = yield pool.submit(executor, x, y)
    print("Got:", result)

if __name__ == '__main__':
    # first we need to create pool executor
    pool = ThreadPoolExecutor(8)
    # and than we can submit the task to it
    Task(do_executor(pool, 2, 3)).step()
    for i in range(20):
        time.sleep(1)
        print(".", end="", flush=True)

