
def yieldfrom(x, y):
    """Simple yield from usage"""
    yield from x
    yield from y

if __name__ == '__main__':
    a = [1, 2, 3]
    b = [4, 5, 6]
    # iterate over function result
    for i in yieldfrom(a, b):
        print(i, end=' ')

    # chain generator calls
    for i in yieldfrom(yieldfrom(a, b), yieldfrom(b, a)):
        print(i, end=' ')
