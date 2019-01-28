layout: true
class: center, middle
background-image: url(img/ugur-akdemir-238673-unsplash.jpg)
---
<br />
## Writing kube controllers for everyone
### Maciej Szulik / @soltysh
### Red Hat

???

What is the first thing that comes to your mind when you hear a word controller.

---
layout: true
class: center, middle
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
]

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
Work queue has a FIFO and a penalty box.

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

???

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
this guy at the bottom, who created it and it is included in the
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


---
## 1.
# Operate on one item at a time

???

Operate on one item at a time. If you use a workqueue.Interface, you'll be able to queue changes for a particular resource and later pop them in multiple “worker” gofuncs with a guarantee that no two gofuncs will work on the same item at the same time.

Many controllers must trigger off multiple resources (I need to "check X if Y changes"), but nearly all controllers can collapse those into a queue of “check this X” based on relationships. For instance, a ReplicaSet controller needs to react to a pod being deleted, but it does that by finding the related ReplicaSets and queuing those.


---
## 2.
# Random ordering between resources

???

Random ordering between resources. When controllers queue off multiple types of resources, there is no guarantee of ordering amongst those resources.

Distinct watches are updated independently. Even with an objective ordering of “created resourceA/X” and “created resourceB/Y”, your controller could observe “created resourceB/Y” and “created resourceA/X”.


---
## 3.
# Level driven, not edge driven

???

Level driven, not edge driven. Just like having a shell script that isn't running all the time, your controller may be off for an indeterminate amount of time before running again.

If an API object appears with a marker value of true, you can't count on having seen it turn from false to true, only that you now observe it being true. Even an API watch suffers from this problem, so be sure that you're not counting on seeing a change unless your controller is also marking the information it last made the decision on in the object's status.


---
## 4.
# Use SharedInformers

???

Use SharedInformers. SharedInformers provide hooks to receive notifications of adds, updates, and deletes for a particular resource. They also provide convenience functions for accessing shared caches and determining when a cache is primed.

Use the factory methods down in https://git.k8s.io/kubernetes/staging/src/k8s.io/client-go/informers/factory.go to ensure that you are sharing the same instance of the cache as everyone else.

This saves us connections against the API server, duplicate serialization costs server-side, duplicate deserialization costs controller-side, and duplicate caching costs controller-side.

You may see other mechanisms like reflectors and deltafifos driving controllers. Those were older mechanisms that we later used to build the SharedInformers. You should avoid using them in new controllers.


---
## 5.
# Never mutate original objects

???

Never mutate original objects! Caches are shared across controllers, this means that if you mutate your "copy" (actually a reference or shallow copy) of an object, you'll mess up other controllers (not just your own).

The most common point of failure is making a shallow copy, then mutating a map, like Annotations. Use api.Scheme.Copy to make a deep copy.


---
## 6.
# Wait for your secondary caches

???

Wait for your secondary caches. Many controllers have primary and secondary resources. Primary resources are the resources that you'll be updating Status for. Secondary resources are resources that you'll be managing (creating/deleting) or using for lookups.

Use the framework.WaitForCacheSync function to wait for your secondary caches before starting your primary sync functions. This will make sure that things like a Pod count for a ReplicaSet isn't working off of known out of date information that results in thrashing.


---
## 7.
# There are other actors in the system

???

There are other actors in the system. Just because you haven't changed an object doesn't mean that somebody else hasn't.

Don't forget that the current state may change at any moment--it's not sufficient to just watch the desired state. If you use the absence of objects in the desired state to indicate that things in the current state should be deleted, make sure you don't have a bug in your observation code (e.g., act before your cache has filled).


---
## 8.
# Re-queue errors

???

Percolate errors to the top level for consistent re-queuing. We have a workqueue.RateLimitingInterface to allow simple requeuing with reasonable backoffs.

Your main controller func should return an error when requeuing is necessary. When it isn't, it should use utilruntime.HandleError and return nil instead. This makes it very easy for reviewers to inspect error handling cases and to be confident that your controller doesn't accidentally lose things it should retry for.


---
## 9.
# Watches and Informers will “sync”

???

Watches and Informers will “sync”. Periodically, they will deliver every matching object in the cluster to your Update method. This is good for cases where you may need to take additional action on the object, but sometimes you know there won't be more work to do.

In cases where you are certain that you don't need to requeue items when there are no new changes, you can compare the resource version of the old and new objects. If they are the same, you skip requeuing the work. Be careful when you do this. If you ever skip requeuing your item on failures, you could fail, not requeue, and then never retry that item again.



---
## 10.
# Use ObservedGeneration when possible

???

If the primary resource your controller is reconciling supports ObservedGeneration in its status, make sure you correctly set it to metadata.Generation whenever the values between the two fields mismatches.

This lets clients know that the controller has processed a resource. Make sure that your controller is the main controller that is responsible for that resource, otherwise if you need to communicate observation via your own controller, you will need to create a different kind of ObservedGeneration in the Status of the resource.


---
## 11.
# Consider using owner references

???



Consider using owner references for resources that result in the creation of other resources (eg. a ReplicaSet results in creating Pods). Thus you ensure that children resources are going to be garbage-collected once a resource managed by your controller is deleted. For more information on owner references, read more here.

Pay special attention in the way you are doing adoption. You shouldn't adopt children for a resource when either the parent or the children are marked for deletion. If you are using a cache for your resources, you will likely need to bypass it with a direct API read in case you observe that an owner reference has been updated for one of the children. Thus, you ensure your controller is not racing with the garbage collector.


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
