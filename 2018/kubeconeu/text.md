layout: true
class: center, middle, inverse
background-image: url(img/kubeconeu.png)
---
<br />
## Writing kube controllers for everyone
### Maciej Szulik / @soltysh
### Red Hat


---
layout: true
class: center, middle
---
background-image: url(img/ugur-akdemir-238673-unsplash.jpg)
.footnote[
https://unsplash.com/photos/5X39cfzKX3o
]

???

What is the first thing that comes to your mind when you hear a word controller.


---
background-image: url(img/cronjob_controller.png)
# ~400 LOC

.footnote[
https://github.com/kubernetes/kubernetes/blob/master/pkg/controller/cronjob/cronjob_controller.go
]

???

Unfortunately, for me the controller always means code.

To be honest, the controller + utils might actually be close 1000 LOC.

If this looks complicated let me try to squeeze the code slightly and present it
to you in a more digestable form.


---
### Control loop
.big-code[
```go
func (c *Ctrl) worker() {
	for c.processNextItem() {
	}
}
```
```go
func (c *Ctrl) processNextItem() {
	item := c.queue.Get()
	err := c.syncHandler(item)
	c.handleErr(err, item)
}
```
]]

???

Basically, every controller after being contructed invokes the worker which
in a loop processes elementes from the queue. That's basically all you need to
know.

I hope you enjoyed this short presentation and you can all head for lunch now!


---
layout: false
class: center, middle, inverse
background-image: url(img/aaron-burden-261332-unsplash.jpg)
# Where do I start?
.footnote[
https://unsplash.com/photos/NZ2SlpcVw1Y
]


---
layout: true
class: center, middle
---
# 30+
# Existing Controllers
<br />
.red[
### Advanced
]

???

There are more than 30 existing controllers, this includes the one you might
have heard about, such as workload controllers (deployments, stateful set,
daemon set, replica set), batch controllers (job and cronjob). As well as
other core controllers that are working behind the scene for you to make
kubernetes awesome!

Do not use cronjob controller as an example, not yet!


---
# Sample controller
.big-text[
https://github.com/kubernetes/sample-controller/
]
.green[
### Entry-level
]


---
# kubebuilder
.big-text[
https://github.com/kubernetes-sigs/kubebuilder
]
.green[
### Entry-level
]


---
layout: false
class: center, middle, inverse
background-image: url(img/chad-kirchoff-202730-unsplash.jpg)
.footnote[
https://unsplash.com/photos/xe-e69j6-Ds
]

???

If you now feel really hungry, but for knowledge not food! Let's actually look under
the hood. Ready?


---
layout: true
class: center, middle
---
### Control loop
.big-code[
```go
func (c *Ctrl) worker() {
	for c.processNextItem() {
	}
}
```
```go
func (c *Ctrl) processNextItem() {
	item := c.queue.Get()
	err := c.syncHandler(item)
	c.handleErr(err, item)
}
```
]

???

I've already shown you the controller loop, but let me refresh your memory.
In the next few minutes we're going to slice and dice this loop into understandable
blocks.


---
# Queue
.big-code[
```go
queue = workqueue.NewNamedRateLimitingQueue(
	workqueue.DefaultControllerRateLimiter(),
	"foos"),
```
]

???

There are several variants of the rate limiters available:
- default rate limiter
- exponential failre rate limiter
- fast slow rate limiter
- combinations of eariler using MaxOfRateLimitters


---
# Shared informers
.big-code[
```go
podInformer = InformerFactory.Core().V1().Pods()
```
]

???

SharedInformer has a shared data cache and is capable of distributing notifications
for changes to the cache to multiple listeners who registered via AddEventHandler.

When you receive a notification, the cache will be AT LEAST as fresh as the notification,
but it MAY be more fresh.  You should NOT depend on the contents of the cache exactly
matching the notification you've received in handler functions.


---
### Shared informers - event handler
.big-code[
```go
podInformer.Informer().AddEventHandler(
	cache.ResourceEventHandlerFuncs{
		// react to newly added object
		AddFunc: func(obj interface{}) {},
		// react to update to the object
		UpdateFunc: func(old, cur interface{}) {},
		// react to object removal
		DeleteFunc: func(obj interface{}) {},
	})
```
]


---
### Shared informers - listers
.big-code[
```go
podStore = podInformer.Lister()
```
]


---
### SyncHandler
.big-code[
```go
func (c *Ctrl) syncHandler(key string) error {
  // Convert into a distinct namespace and name
  ns, name, err := cache.SplitMetaNamespaceKey(key)
  // Get the object
  podTmp, err := c.podsLister.Pods(ns).Get(name)
  // !!! IMPORTANT !!!
  pod := podTmp.DeepCopy()
  // ... your logic goes here ...
  return nil
}
```
]

???

This is the brain of the controller and where you can finally start cranking
your awesome logic!


---
layout: false
class: center, middle, inverse
background-image: url(img/client-go-controller-interaction.jpeg)
.footnote[
https://github.com/devdattakulkarni
]

???

Let me recap what I told you so far as a nice picture, all credit goes to
this guy at the bottom, who created it and it is meant to be included in the
sample-controller repository for future controller authors like you!


---
layout: true
class: center, middle
---
# Controller ground rules
<br />
https://github.com/kubernetes/community/blob/master/contributors/devel/controllers.md

???

As a closing remark lemme point you to the ground rules every good citizien of
kube ecosystem should follow:

1. Operate on one item at a time.
2. Random ordering between resources.
3. Level driven, not edge driven.
4. Use SharedInformers.
5. Never mutate original objects!
6. Wait for your secondary caches.
7. There are other actors in the system.
8. Percolate errors to the top level for consistent re-queuing.
9. Watches and Informers will “sync”.
10. If the primary resource your controller is reconciling supports ObservedGeneration in its status, make sure you correctly set it to metadata.Generation whenever the values between the two fields mismatches.
11. Consider using owner references for resources that result in the creation of other resources.


---
layout: false
class: center, middle, inverse
background-image: url(img/jon-tyson-518780-unsplash.jpg)
.pull-left[
## @soltysh
]
.footnote[
https://unsplash.com/photos/RUsczRV6ifY
]
