
Typical generator function, using `yield` statement:

```
def countdown(n):
    while n > 0:
        yield n
        n =- 1
```

Typical usage:

```
for x in countdown(10):
    print("We've got ", x)
```

Basically every function written using yield statement is a generator, which
can than be used to feed all kinds of loops and iterations.

Under the cover iteration calls `next()` to get the next value from generator,
until it reaches `StopIteration` exception.

```
>>> c = countdown(3)
>>> c
<generator object countdown at 0x7f62b5c58090>
>>> next(c)
3
>>> next(c)
2
>>> next(c)
1
>>> next(c)
Traceback (most recent call last):
  File "stdin", line 1, in ?
    print(next(c))
StopIteration

This is just the beginning, and more is to come in a second.

Generators as pipelines -> explored in 1st tutorial, must be here!!!!

What's probably lesser known functionality is that `yield` statement can be used
to receive values.

```
def receiver():
    while True:
        item = yield
        print("Got: ", item)
```

```
>>> c = receiver()
>>> c
<generator object countdown at 0x7f62b5c58090>
>>> next(c)
>>> c.send(43)
('Got: ', 43)
>>> c.send([1, 2, 3])
('Got: ', [1, 2, 3])
>>> c.send("Hello")
('Got: ', 'Hello')
```

These are called couroutines -> explored in 2nd tutorial, must be here!!!

*Any* function having `yield` statement in it's body is actually generator,
it's not gonna to execute, it'll return *generator object*. Starting from here
you can do following operations:
* `next()` - advance code to `yield` statement and emit value, if such  was passed
  as a parameter, that's the only operation you can call after creating generator.
* `send()` - sends value to `yield` statement making it produce value instead of
  emitting, remember to call `next()` beforehand
* `close()` - closing generator is a way to inform it that it should finish his work,
  it generates `GeneartorExit` exception upon calling `yield` statement
* `throw()` - give you opportunity to send an error to generator upon call to `yield`
  statement

In Python 3 you can have both `yield` and `return` statement, in previous python
version that was syntax error. Currently it means

```
def returnyield(x):
    """Using return in generator"""
    yield x
    return "Hi there"
```

```
>>> ry = returnyield(5)
<generator object returnyield at 0x7f0fb6335090>
>>> print(ry)
5
>>> print(ry)
Traceback (most recent call last):
  File "returnyield.py", line 14, in <module>
    print(next(ry))
StopIteration: Hi there
```

Generator delegation, PEP-380 -> `yield from`
You're passing the generation to other function.

```
def yieldfrom(x, y):
    yield from x
    yield from y
```

```
>>> x = [1, 2, 3]
>>> y = [4, 5, 6]
>>> for i in yieldfrom(x, y):
...     print(i)
1
2
3
4
5
6
```

These both `yield from` statements took values from both lists, consume them
and spit them as it they were one list. So in it's simplest form these can
be seen as hidden for loops, but soon you'll see there's more to it than just
this. What else can be done from here is chaining meaning iteration can be
delegated even further.

If now we would create something like this:

```
for i in yieldfrom(yieldfrom(a, b), yieldfrom(b, a)):
    print(i, end=' ')
```

What this piece of code will do is, the outer most call will delegate iteration
to the inner generators.


I guess you are familliar with constructs such as those:

```
file = open()
... # do some stuff with f
file.close()
```

```
lock.acquire()
... # do some stuff with lock
lock.release()
```

etc.

These are nicely handled currently by ContextManagers, which are basically
normal objects implementing two methods:
* `__enter__(self)` - you're basically staring work with your object, returning it
* `__exit__(self, exc, val, tb)` - you're releasing the object here, or handle
  exception here

So having a context manager such as this:

```
class tempdir(object):
    def __enter__(self):
        self.dirname = tempfile.mkdtemp()
        return self.dirname
    def __exit__(self, exc, val, tb):
        shutil.rmtree(self.dirname)
```

Can be than run as:

```
with tempdir() as dirname:
    print(dirname, os.path.isdir(dirname))
```

Which will return the temporary directory name and the result of a existance check.

Exactly the same code can be rewriten as following:

```
@contextmanager
def tempdir():
    dirname = tempfile.mkdtemp()
    try:
        yield dirname # here the magic happens
    finally:
        shutil.rmtree(dirname)
```

And basically the usage is the same, the only difference is how you define your
context manager. In the later example the decorator is creating the context
manager for you.

Paste here code how @contextmanager decorator looks like!!!
And be sure to check the overhead added by using @contextmanager.

PEP-343

The purpose of this decorator is to simplify write context managers. More of
this in a minute...


Async processing

```
main thread
.
.
run_async(func, args) # in seperate thread
.
.
.
get the result
```

So we have such a pisce of code as a very common programming pattern:

from concurrent.futures import ThreadPoolExecutor

```
def executor(x, y):
    import time
    time.sleep(10)
    return x + y
```

And we can use it as:

```
pool = ThreadPoolExecutor(8)
fut = pool.submit(executor, 2, 3)
fut.result()
```

Above code basically runs in a different thread, and you can either wait for the
execution to finish or create a callback function that will take care of the
result.

```
def handle_result(result):
    """Handling result from previous function"""
    print("Got: ", result.result())

fut.add_done_callback(handle_result)
```

If exeception will happend it will return when getting the result.

See twisted callbacks.

start at 32:00
