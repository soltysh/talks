layout: true
class: center, middle, inverse
background-image: url(img/kubeconeu.png)
---
## Writing kube controllers for everyone
### Maciej Szulik / @soltysh


---
layout: true
class: center, middle
---
background-image: url(img/ugur-akdemir-238673-unsplash.jpg)
.footnote[
https://unsplash.com/photos/5X39cfzKX3o
]


---
background-image: url(img/cronjob_controller.png)
# 409 LOC

.footnote[
https://github.com/kubernetes/kubernetes/blob/master/pkg/controller/cronjob/cronjob_controller.go
]


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


---
# Queue
.big-code[
```go
queue = workqueue.NewNamedRateLimitingQueue(
	workqueue.DefaultControllerRateLimiter(),
	"foos"),
```
]


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
### Shared informers - listers
.big-code[
```go
podStore = podInformer.Lister()
```
]


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


---
layout: false
class: center, middle, inverse
background-image: url(img/client-go-controller-interaction.jpeg)
.footnote[
https://github.com/devdattakulkarni
]


---
layout: true
class: center, middle
---
# Controller ground rules
<br />
https://github.com/kubernetes/community/blob/master/contributors/devel/controllers.md

???

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
.footnote[
https://unsplash.com/photos/RUsczRV6ifY
]
