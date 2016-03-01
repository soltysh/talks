from concurrent.futures import ThreadPoolExecutor
import time

def executor(x, y):
    """Execution of very complex task asynchronously"""
    print("I'm going to sleep for a while...")
    time.sleep(10)
    return x + y

def handle_result(result):
    """Handling result from previous function"""
    print("Got: ", result.result())

if __name__ == '__main__':
    # first we need to create pool executor
    pool = ThreadPoolExecutor(8)
    # and than we can submit the task to it
    fut = pool.submit(executor, 2, 3)
    # and get the result
    print(fut.result())
    print("We're blocked until we get the result...")
