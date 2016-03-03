name: title
layout: true
class: center, middle, inverse
---
# Getting the Jobs Done With
# Kubernetes / OpenShift
.footnote[Maciej Szulik, KubeCon 2016]


---
layout: false
.left-column[
## @soltysh
]
.right-column[
.center[
# .awesome[.fa-twitter[] .fa-github[] .fa-google[] .fa-bitbucket[]]
[maszulik@redhat.com]()
]

https://github.com/soltysh/talks/tree/master/2016/kubecon

.center[
![qr](img/qr.png)
]]


---
name: title
layout: true
class: center, middle, inverse
---
# Job

???
kubectl run hello --image=python:3.5.1 --restart=Never -- python -c 'print("Hello world!")'


---
layout: false
.left-column[
## Job
]
.right-column[
```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: hello
spec:
  template:
    metadata:
      name: hello
    spec:
      containers:
      - name: hello
        image: python:3.5.1
        command: ["python", "-c",
                  "print('Hello world!')"]
      restartPolicy: Never
```
]


---
.left-column[
## Job
### - api
]
.right-column[
.bold[
```yaml
-> apiVersion: batch/v1
```
]
```yaml
kind: Job
metadata:
  name: job
spec:
  template:
    metadata:
      name: job
    spec:
      containers:
      - name: job
        image: python:3.5.1
        command: ["python", "-c",
                  "print('Hello world!')"]
      restartPolicy: Never
```
]


---
.left-column[
## Job
### - api
### - command
]
.right-column[
```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: job
spec:
  template:
    metadata:
      name: job
    spec:
      containers:
```
.bold[
```yaml
->      - name: job
          image: python:3.5.1
          command: ["python", "-c",
                    "print('Hello world!')"]
```
]
```yaml
      restartPolicy: Never
```
]


---
.left-column[
## Job
### - api
### - command
### - restart policy
]
.right-column[
```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: job
spec:
  template:
    metadata:
      name: job
    spec:
      containers:
      - name: job
        image: python:3.5.1
        command: ["python", "-c",
                  "print('Hello world!')"]
```
.bold[
```yaml
->      restartPolicy: Never
```
]]


---
.left-column[
## Job
### - api
### - command
### - restart policy
]
.right-column[
.center[
# Always
# OnFailure
# Never
]]


---
.left-column[
## Job
### - api
### - command
### - restart policy
]
.right-column[
.center[
# ~~Always~~
# OnFailure
# Never
]]


---
.left-column[
## Job
### - api
### - command
### - restart policy
### - pod selector?
]
.right-column[
```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: job
spec:
  template:
    metadata:
      name: job
    spec:
      containers:
      - name: job
        image: python:3.5.1
        command: ["python", "-c",
                  "print('Hello world!')"]
      restartPolicy: Never
```
]


---
.left-column[
## Future
]
.right-column[
## [workflow](http://releases.k8s.io/master/docs/proposals/workflow.md) by @sdminonne
## [indexed jobs](http://releases.k8s.io/master/docs/design/indexed-job.md) by @erictune
## [scheduled jobs](http://releases.k8s.io/master/docs/proposals/scheduledjob.md) by @soltysh
]

---
.left-column[
## Links
]
.right-column[
### soltysh @ .awesome[.fa-twitter[] .fa-github[] .fa-google[] .fa-bitbucket[]]
[maszulik@redhat.com]()


http://releases.k8s.io/master/docs/proposals/job.md

http://releases.k8s.io/master/docs/user-guide/jobs.md

]
