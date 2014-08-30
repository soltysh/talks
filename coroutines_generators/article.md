One of the hottest topics, most frequently mentioned, since python3.4 was
introduced is asyncio module, introduced in [PEP 3156](http://legacy.python.org/dev/peps/pep-3156/).
In the following article I'll try to show you some cool stuff that lies at the
core of this module. But before we dig in, one warning, most of the samples
presented in this article are written with python3.4 in mind, so make sure
to use at least that version when running examples which are available at
[my github account](https://github.com/soltysh/talks/tree/master/coroutines_generators/examples).

Let's start with this sample piece of code
[generator1.py](https://github.com/soltysh/talks/tree/master/coroutines_generators/examples/generator1.py):

```
def countdown(n):
    while n > 0:
        yield n
        n =- 1
```

As you've probably noticed this is the simplest generator function you
can think of. It's typical usage is as following:

```
for x in countdown(10):
    print("Got ", x)
```

This basically print every number starting from 10 down to 1. So we can conclude
that every function written using `yield` statement is a generator, which
can than be used to feed all kinds of loops and iterations. If we look under
the cover this iteration calls `next()` to get the next value from generator,
until it reaches `StopIteration` exception. We can illustrate that with following
piece of code:

```
c = countdown(3)
print(c)
next(c)
next(c)
next(c)
next(c)
```

The result of running this code is:

```
<generator object countdown at 0x7f2b0fa7a0d0>
3
2
1
Traceback (most recent call last):
  File "generator1.py", line 21, in <module>
    print(next(c))
StopIteration
Traceback (most recent call last):
  File "stdin", line 1, in ?
    print(next(c))
StopIteration
```

This is of course just the beginning, to make sure everybody will reach the
same level of knowledge. So expect more of the promised awesomeness to come.

TODO:
!!!Generators as pipelines -> explored in 1st tutorial, must be here!!!

What's probably lesser known fact, is that `yield` statement can be used
to receive values. See [generator2.py](https://github.com/soltysh/talks/tree/master/coroutines_generators/examples/generator2.py):

```
def receiver():
    while True:
        item = yield
        print("Got: ", item)

c = receiver()
print(c)
next(c)
c.send(43)
c.send([1, 2, 3])
c.send("Hello")
```

Output of this code is following:

```
<generator object receiver at 0x7f1690d88f58>
Got:  43
Got:  [1, 2, 3]
Got:  Hello
```

TODO:
!!!These are called couroutines -> explored in 2nd tutorial, must be here!!!

So at this point we can conclude that *any* function having `yield` statement
in it's body is actually generator. Meaning it's not gonna to execute, but
it'll return *generator object*, which provides following operations:
* `next()` - advance code to `yield` statement and emit value, if such was
  passed as a parameter. That's the *only* operation you can call after
  creating generator.
* `send()` - sends value to `yield` statement making it produce value instead
  of emitting. *Remember* to call `next()` beforehand.
* `close()` - closing generator is a way to inform it that it should finish
  his work. It generates `GeneartorExit` exception upon calling `yield`
  statement.
* `throw()` - gives you opportunity to send an error to generator upon call
  to `yield` statement.


In Python 3.4 specifically you can have both `yield` and `return` statement,
in previous python versions that was syntax error. Currently if you write,
[generator3.py](https://github.com/soltysh/talks/tree/master/coroutines_generators/examples/generator3.py):

```
def returnyield(x):
    yield x
    return "Hi there"

ry = returnyield(5)
print(ry)
print(next(ry))
print(next(ry))
```

Output of above code is following:

```
<generator object returnyield at 0x7f27bf38bf58>
5
Traceback (most recent call last):
  File "generator3.py", line 15, in <module>
    print(next(ry))
StopIteration: Hi there
```

If you carefully study the output you'll notice that the value of the `return`
statement was actually passed as value of the `StopIteration` exception.
Interesting isn't it?

Let's move forward than. [PEP 380](http://legacy.python.org/dev/peps/pep-0380/)
introduced the concept of generator delegation. This basically means that
instead of manually iterating, we're passing the generation to sombody else,
who will do it for us, as presented in
[yieldfrom.py](https://github.com/soltysh/talks/tree/master/coroutines_generators/examples/yieldfrom.py):

```
def yieldfrom(x, y):
    yield from x
    yield from y

x = [1, 2, 3]
y = [4, 5, 6]
for i in yieldfrom(x, y):
     print(i, end=' ')
```

Expected output is series of number starting from 1 until 6. What happened here
is that both these `yield from` statements took values from both lists, consume
them and spit them as if they were one list. So in it's simplest form, these can
be seen as hidden for loops, but soon you'll see there's more to it. What else
can be done from here is chaining, meaning iteration can be delegated even
further. Let's create something more complicated:

```
for i in yieldfrom(yieldfrom(a, b), yieldfrom(b, a)):
    print(i, ' ')
```

What this piece of code will do is, the outer most call will delegate iteration
to the inner generators and further down until we reach single value that will
be yielded.

Moving further ahead, I'm hoping the reader is familiar with these constructs:

```
file = open()
# do some stuff with f
file.close()

lock.acquire()
# do some stuff with lock
lock.release()
```

These constructs are currently nicely handled by context managers, introduced
with `with` statement, see [PEP 343](http://legacy.python.org/dev/peps/pep-0343/),
which are basically normal objects implementing two methods:
* `__enter__(self)` - star work with your object, returning it
* `__exit__(self, exc, val, tb)` - release the object, or handle the exception

We can create sample context manager for working with temporary directory,
[contextmanager1.py](https://github.com/soltysh/talks/tree/master/coroutines_generators/examples/contextmanager1.py):

```
class tempdir(object):
    def __enter__(self):
        self.dirname = tempfile.mkdtemp()
        return self.dirname
    def __exit__(self, exc, val, tb):
        shutil.rmtree(self.dirname)

with tempdir() as dirname:
    print(dirname, os.path.isdir(dirname))
```

This sample context manager will create a temporary directory, which name we
print and then check for it's existence.

Thanks to awesome python core devs, `yield` and `@contextmanager` the same code
can be rewritten,
[contextmanager2.py](https://github.com/soltysh/talks/tree/master/coroutines_generators/examples/contextmanager2.py):

```
@contextmanager
def tempdir():
    dirname = tempfile.mkdtemp()
    try:
        yield dirname # here the magic happens
    finally:
        shutil.rmtree(dirname)
```

One will use this piece of code exactly the same way as previous context manager.
The only difference is how you define your context manager. In the later example
the decorator is creating the context manager for you, and `yield` returns the
temporary directory. If you look under the cover you'll see that calling
`tempdir()` in the first example will return `<__main__.tempdir object at 0x7f3e4778f5a0>`
whereas the later `<contextlib._GeneratorContextManager object at 0x7fd94c7ce538>`.
Do you see the difference? If you look under the cover of `@contextmanger`
decorator you'll find out that what it does it sets up the `__enter__` and
`__exit__` methods with some additional error checking for you, see
[contextlib.py#96](http://hg.python.org/cpython/file/ab81b4cdc33c/Lib/contextlib.py#l96).
For those of you concerned about performance, I've tested it and the decorator
solution runs ~9% slower than it's class counterpart. But think how much the
decorator solution is easier to read.

<!--
The purpose of this decorator is to simplify write context managers. More of
this in a minute...
 -->

Finally we've reached the last part - asynchronous processing. The usual way
of processing in those cases is: we have some main thread, in it we run some
asynchronous function, and after some time we reach for the results.
This very common programming pattern can be presented with following code,
[future1.py](https://github.com/soltysh/talks/tree/master/coroutines_generators/examples/future1.py):

```
def executor(x, y):
    time.sleep(10)
    return x + y

pool = ThreadPoolExecutor(8)
fut = pool.submit(executor, 2, 3)
fut.result()
```

Above code basically runs in a different thread, and you can either wait for the
execution to finish or create a callback function that will take care of the
result. Waiting means blocking we're blocked until we get the result, but the
latter means we still have control in main thread and the result will get back
to us when it's ready, [future2.py](https://github.com/soltysh/talks/tree/master/coroutines_generators/examples/future2.py):

```
def handle_result(result):
    """Handling result from previous function"""
    print("Got: ", result.result())

pool = ThreadPoolExecutor(8)
fut = pool.submit(executor, 2, 3)
fut.add_done_callback(handle_result)
```

Quick note, if exception will happen inside the executor method it will be
returned when getting the result. Testing this will be left as an exercise to
the reader.

OK, we've reached a point where I've showed you a couple cool tricks with
generators, but you may ask how it's useful? What can we do about it? Let's than
move to the final part where I'll show you how using previous tricks we can
bypass certain python limitations and create asyncio core functionality.

Let's start with creating a task object, which is basically what I've showed
just before, but this time, we'll pack the idea into a reusable object,
[task.py](https://github.com/soltysh/talks/tree/master/coroutines_generators/examples/task.py):

```
class Task:
    def __init__(self, gen):
        self._gen = gen

    def step(self, value=None):
        try:
            fut = self._gen.send(value)
            fut.add_done_callback(self._wakeup)
        except StopIteration as exc:
            pass

    def _wakeup(self, fut):
        result = fut.result()
        self.step(result)
```

If you look at the above you'll notice the code is almost identical to previous
with one, with `ThreadPoolExecutor` placed inside of a sort of context manager
class presented couple examples before. The only difference being method names,
`step()` in place of `__enter__` and `_wakeup()` for `__exit__()`. What we have
here actually, is a task object accepting generator as the only initialization
parameter, with main function `step()` responsible for proceeding with
execution to the next yield statement and a callback to do something with
the result. So how you can use it

!!! Think about adding Task thing from presentation ~42min.

Must be Task, as this is how asyncio works.

Check http://legacy.python.org/dev/peps/pep-0342/

yield from generator is basically transferring control to subgenerators.

Don't forget to add example how to bypass sys.getrecursionlimit() which is 1000,
using Task and recursive function. As well as to show that even though we're using
ThreadPoolExecutor we are doing job faster, no GIL problem!

ended @ 1:16:30
