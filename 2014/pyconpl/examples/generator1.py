
def countdown(n):
    """The simplest generator"""
    while n > 0:
        yield n
        n -= 1

if __name__ == '__main__':
    # usual generator usage
    for c in countdown(3):
        print(c)

    # under the cover it does:
    # create generator
    c = countdown(3)
    print(c)
    # continute to the next value
    print(next(c))
    print(next(c))
    print(next(c))
    print(next(c))
