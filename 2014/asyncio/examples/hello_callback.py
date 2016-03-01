import asyncio
import time

def print_and_repeat(loop):
    print(time.strftime("%H:%M:%S"), 'Hello World')
    loop.call_later(2, print_and_repeat, loop)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    print_and_repeat(loop)
    loop.run_forever()
