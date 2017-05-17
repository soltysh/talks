name: title
layout: true
class: center, middle, inverse
---
.center[
# bugs.python.org
<br />
## Maciej Szulik / @soltysh
### Red Hat / OpenShift
]


---
layout: false
.center[
.pull-left[.center[
###Shiyao Ma

2015 - dockerize bpo

![Shiyao Ma](https://bitbucket.org/account/introom/avatar/256/?ts=1494893474)

https://bitbucket.org/introom/
]]

.pull-right[.center[
### Anish Shah
2016 - bpo - gh integration

![Anish Shah](https://avatars3.githubusercontent.com/u/3175743?v=3&s=400)

https://github.com/AnishShah
]]]


---
.left-column[
# Current state
]

.right-column[
## Linking PRs with
### `bpo-XXXX`

- title (setting or updating)
- initial pull request description
- pull request comments
- review comments

.red[Limited to 10!]

<br />

## Closing issues on merge with
###`close[sd]?|closing bpo-XXXX`
]


---
.left-column[
# Running locally
## - short version
]
.right-column[
<br />
<br />

.big-code[
```bash
docker run --rm \
    -it -p 9999:9999 \
    -v `pwd`:/opt/tracker \
    soltysh/b.p.o
```
]]


---
.left-column[
# Running locally
## - full version ;-)
]
.right-column[
```bash
# clone roundup
hg clone https://hg.python.org/tracker/roundup
cd roundup
hg update bugs.python.org

# clone and setup python specifics
hg clone https://hg.python.org/tracker/python-dev
cd python-dev
mkdir db
echo postgresql > db/backend_name
cp config.ini.template config.ini
cp detectors/config.ini.template detectors/config.ini

# clone docker image and build it
git clone git@github.com:python/docker-bpo.git
cd docker-bpo
make USERNAME=soltysh

# while at the dir where roundup and python-dev are cloned
docker run --rm -it -p 9999:9999 -v `pwd`:/opt/tracker soltysh/b.p.o

rd-start
```

### Don't forget to add .red[:Z] when using SELinux:
```bash
-v `pwd`:/opt/tracker:Z
```
]


---
.left-column[
# The Future
]
.right-column[
<br />
## 1. Google OAuth integration
<br />
## 2. Github OAuth integration
<br />
## 3. Escalate to support vendor
]
]


---
name: title
layout: true
class: center, middle, inverse
---
# Questions?
<br />
.large[.center[
http://psf.upfronthosting.co.za/roundup/meta/
]]
<br /><br />
## Maciej Szulik / @soltysh
### Red Hat / OpenShift
