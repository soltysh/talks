import asyncio
import time

@asyncio.coroutine
def greet_every_two_seconds():
    while True:
        print(time.strftime("%H:%M:%S"), 'Hello World')
        yield from asyncio.sleep(2)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(greet_every_two_seconds())
