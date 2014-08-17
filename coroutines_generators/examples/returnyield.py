
def returnyield(x):
    """Using return in generator"""
    yield x
    # available only in python3!!!
    return "Hi there"

if __name__ == '__main__':
    # create generator
    ry = returnyield(5)
    print(ry)
    # advance to next value
    print(next(ry))
    # this call throws StopIteration error with return's value
    print(next(ry))
