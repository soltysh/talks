
def receiver():
    """Using yield as a receiver"""
    while True:
        item = yield
        print("Got: ", item)

if __name__ == '__main__':
    # create generator
    c = receiver()
    print(c)
    # advance to yield
    next(c)
    # now you can send stuff
    c.send(43)
    c.send([1, 2, 3])
    c.send("Hello")
