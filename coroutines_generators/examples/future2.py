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
    # and the callback function as well
    fut.add_done_callback(handle_result)
    # to prove that we still have control in main thread
    for i in range(20):
        time.sleep(1)
        print(".", end="", flush=True)
