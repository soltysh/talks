## Async I/O ##

### Maciej Szulik ###

### soltysh @ <i class="fa-twitter"></i><i class="fa-github"></i><i class="fa-bitbucket"></i> ###

Katowice, 2014


## TOC ##

* Synchronous vs. Threaded vs. Asynchronous
* Asynchronous I/O
* Architecture
* Examples
* Q & A


## Synchronous ##

![Synchronous](img/sync.png)\ 


## Threaded ##

![Synchronous](img/sync.png)
![Threaded](img/threaded.png)


## Asynchronous ##

![Synchronous](img/sync.png)
![Threaded](img/threaded.png)
![Asynchronous](img/async.png)


## Asynchronous I/O ##

* `select`, `poll`, `kqueue`
* I/O Completion Ports
* asyncore


## Asynchronous I/O ##

![KeepCalm](img/keepcalm.png)\ 


## Asynchronous I/O ##

* Asynchronous frameworks:
    - Twisted
    - Tornado
    - Stackless Python
* asyncio (PEP-3156)


## Asynchronous I/O ##

* Usability
* Interoperability
* Multiplatform
* TCP & UDP support
* IPv4 & IPv6 support
* Pipes, subprocesses, etc.
* Standard library (no 3rd party dependency)
* Almost pure python


## Architecture ##

* Coroutines, Futures, Tasks
* Event loop
* Transport & Protocols


## Coroutines et all ##

* Coroutines - `@coroutine` & `yield from`
* Future - object with result
* Task - variant (subclass) of a Task


## Event loop ##

* Multiplexes different activities
* Managing:
    - `get_event_loop`
    - `set_event_loop`
    - `new_event_loop`
    - `stop`
    - `close`
    - `is_running`
* No nested loops


## Event loop ##

* Coroutines:
    - `run_forever`
    - `run_until_complete`
* Callbacks:
    - `call_soon`
    - `call_later`
    - `call_at`
    - _No repeated callback_


## Transport & Protocol ##

* Transport -> socket, pipe
* Protocol -> your application
* Client & server


## Examples ##


## Pros & Cons ##

![Turtle vs. Rabbit](img/turtlerabbit.png)\ 


## Pros & Cons ##

* small memory footprint
* ~ fast I/0
* python built-in

* young project
* python 3.4+


## Summary ##

* python 3.4+
* https://code.google.com/p/tulip/
* https://groups.google.com/forum/?fromgroups#!forum/python-tulip
* http://www.python.org/dev/peps/pep-3156/
* http://www.youtube.com/watch?v=1coLC-MUCJc
* http://www.youtube.com/watch?v=c7D63mqCs5Y


## Questions? ##

![Questions](img/questions.png)\


#### Maciej Szulik ####

#### soltysh @ <i class="fa-twitter"></i><i class="fa-github"></i><i class="fa-bitbucket"></i> ####

