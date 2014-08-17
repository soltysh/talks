
def countdown(n):
    while n > 0:
        yield n
        n -= 1

def receiver():
    while True:
        item = yield
        print("Got: ", item)

if __name__ == '__main__':
    c = receiver()
    print(c)
    next(c)
    c.send(43)
    c.send([1, 2, 3])
    c.send("Hello")
