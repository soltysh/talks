layout: true
class: center, middle
---
# The new life of bugs.python.org
<br /><br />
### Maciej Szulik / @soltysh


---
background-image: url(img/todd-quackenbush-701.jpg)

???

This presentation is covering the current work I'm doing on migrating
bugs.python.org to OpenShift. It's in now way complete, there are many
moving pieces, but let the facts speak for itself.


---
background-image: url(img/bpo.png)
.footnote[
http://roundup.sourceforge.net/
]
???

bugs.python.org is a bug tracker supporting the development of the CPython, which is
the references implementation of Python language. In short the most popular Python and
most probably the one you are already using.
The system itself is a very simple system web app, written in python, obviously. It is called
roundup.

Back in May last year, during PyCon US in Portland, Oregon I was approached by Brett Cannon
and Mark Mangoba with a task to migrate current BPO instance to a new place. My initial reaction
was 'Let's OpenShift Online for that', and the rest as they say is a history, well almost ;)

---
background-image: url(img/thomas-kvistholt-191153.jpg)

???

Upon inspecting the current deployment details I found that:
1. I need to run roundup
2. I need to run postgresql
None of this was new to me, since I've been supporting bugs.python.org for more than
2 years now. I won't bore you with the exact deployment details of the current instance
since in some time it'll be history, so let's focus on the future instead.
And so, armed with the knowledge about how bpo works, and dirty details of the current
deployment soon to be replaced I jumped into work.


---
# Get the app
# in a container

???

The first step was put the entire app as is inside a container and try running it.
But actually that step was already handled for me by a PSF's GSoC student a few years
back. He created a docker image which would allow for a local development of BPO. For that
he deserves a big round of aplause! So instead of starting from scartch I actually based
my work on top of his.


---
## docker run
## python/docker-bpo
.footnote[
https://github.com/python/docker-bpo/
]

???

It also happens that we publish BPO image on our official dockerhub account, so that anyone
interested can help with BPO fixes :) In short, this image mounts a local directories with
BPO sources and launches both PostgreSQL and roundup for you. Since I've been using since
the early days of my BPO time I was very familiar with the entire structure of the image.


---
# Builder image

???

All I needed was how to split the all-in-one image with mountable source code into separate
pieces. The first step was to be able to build a BPO instance from sources.


---
## Source-to-Image

.footnote[
https://github.com/openshift/source-to-image
]

???

I could not use any of the official builder images provided by OpenShift because
bpo components are kept in mercurial repository and S2I supports git, by default.
Moreover, there are two repositories (one with the roundup installation with some
BPO specific bits, and second where the majority of customization is placed) you
need so that's again not supported in S2I.

I ended up building an S2I builder based on the article I wrote a while ago
(https://blog.openshift.com/create-s2i-builder-image/). In short, one needs
to write:
1. Dockerfile for the image.
2. S2I scripts (assemble & run).

---

## https://github.com/python/bpo-builder/


---
# Database

???

Initially, we were planning to use an externally hosted database, something like
Amazon RDS or similar. This significantly simplified my work, because I didn't care
about the database part at all. I've used a temporary PostgreSQL instance one can
easily setup on OpenShift and worry about a thing.


---
#### oc cluster up

# Put it all together

#### and enjoy

???

With both of the bits figured out I was confident that I'm ready for my full build
and deployment workflow for bugs.python.org. That was pretty bold, especially with
my current knowledge ;)


---
#### Initial build

# Finished successfully

???

While building the builder image I was also using the s2i CLI for testing if it's
working as it should this step unsurprisingly finished fast and without any problems.
A few observations I've had back then was that I should probably improve the logging
information so that it's clear what is being built and from where, since from start
I allowed specifying different repository URLs through environment variables injected
into build configuration.


---
#### Initial deployment

```python
WARNING: The database is already initialised!
If you re-initialise it, you will lose all the data!
Traceback (most recent call last):
  File "/opt/tracker/bin/roundup-admin", line 15, in <module>
    run()
  File "/opt/tracker/roundup/roundup/scripts/roundup_admin.py", line 49, in run
    sys.exit(tool.main())
  File "/opt/tracker/roundup/roundup/admin.py", line 1635, in main
    ret = self.run_command(args)
  File "/opt/tracker/roundup/roundup/admin.py", line 1504, in run_command
    return self.do_initialise(self.tracker_home, args)
  File "/opt/tracker/roundup/roundup/admin.py", line 536, in do_initialise
    Erase it? Y/N: """))
EOFError: EOF when reading a line
```

???

With way too much optimism I moved to the second part of the flow - the deployment.
While the build was kicking in I quickly deployed the latest available PostreSQL
image and waited impatiently for the initial deplyment, which obviously failed.
The problem was with the way how roundup initiates database, if database exists
it assumes it was already initiated, but since it's empty it won't run. That's
sort of the chicken and egg problem. Eventually, I went with two deployments
one which was initiating the database and a second that was using the already
initialized database. For that I use an environment variable. So that the production
system isn't accidentally erased (sic!). This also required some manual intervention
on the PostgreSQL end: removing the database and giving higher privileges for the
roundup user.


---
#### Initial deployment cont'd

```python
Traceback (most recent call last):
  File "/opt/tracker/bin/roundup-server", line 11, in <module>
    run()
  File "/opt/tracker/roundup/roundup/scripts/roundup_server.py", line 978, in run
    httpd = config.get_server()
  File "/opt/tracker/roundup/roundup/scripts/roundup_server.py", line 633, in
    get_server for (name, home) in tracker_homes])
  File "/opt/tracker/roundup/roundup/instance.py", line 327, in open
    return Tracker(tracker_home, optimize=optimize)
  File "/opt/tracker/roundup/roundup/instance.py", line 102, in __init__
    self.detectors = self.get_extensions('detectors')
  File "/opt/tracker/roundup/roundup/instance.py", line 207, in get_extensions
    self._execfile(os.path.join(dirname, name), env)
  File "/opt/tracker/roundup/roundup/instance.py", line 239, in _execfile
    self._exec(self._compile(fname), env)
  File "/opt/tracker/roundup/roundup/instance.py", line 233, in _exec
    exec(obj, env)
  File "/opt/tracker/python-dev/detectors/autonosy.py", line 8, in <module>
    from roundup.anypy.sets_ import set
ImportError: No module named sets_
```

???

After solving the database issue I re-run the deployment as previously described
and unfortunately I was surprised with yet another unexpected problem. Sometime
last year Ezio Melotti, who is one of the few of us actively maintaining bpo,
performed a roundup update to catch up the latest updates. It appears that during
this update parts of our customization relied on an old module which was released
in that upgrade. Since none of the places builds the application from scratch
all the places: production, Ezio's and mine workspaces were working due to previously
built pyc files. Since I've perform a clean build from a source repository this
problem was caught immediately. Shortly after syncing with Ezio I submitted a proper
fix to our main repository.


---
background-image: url(img/invalid_url.png)

???

And with all that in place I was able enjoy my first installment of bugs.python.org
on OpenShift.

---
# Configuration

???

Next task was to split the configuration bits.

---
background-image: url(img/success.png)

.footnote[
http://test.bugs.python.org/
]


---
background-image: url(img/ambreen-hasan-346960.jpg)


---
# Database

## part 2

.footnote[
https://github.com/zalando/patroni/
]

---
# What's
# next?

---
background-image: url(img/emily-morter-188019.jpg)

.footnote[
https://unsplash.com/
]
