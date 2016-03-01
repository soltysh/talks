name: title
layout: true
class: center, middle, inverse
---
# How a Java dev benefited
# from transitioning to Go
.footnote[Maciej Szulik, DevConf 2016]


---
.pull-left[![gopher](img/gopher.png)]
.pull-right[![duke](img/duke.png)]
# vs


---
layout: false
.left-column[
## Agenda
]
.right-column[
1. Benefits from transition

1. Java and Go comparison:

  * Types

  * General Syntax

  * Data Structures

  * Interfaces

  * Concurrency

  * Testing

1. Summary
]


---
.left-column[
## @soltysh
]
.right-column[
## .awesome[.fa-twitter[] .fa-github[] .fa-google[] .fa-bitbucket[]]

### +10 years of experience
### C/C++ -> Java
### Java -> Go
### Python
### OpenShift / Red Hat
]


---
.left-column[
## Opinions
]
.right-column[
```
> don't switch
> I miss debugging
> and knowing my interfaces
> and generics
> and collections
> and good logging frameworks
> I miss machine-driven refactors that just
  worked
```
]

--
.right-column[
```
> i do think gofmt was a brilliant move
> having to never think about those issues
  has been awesome
```
]

--
.right-column[
```
> i miss it
> there's plenty i miss about the JVM
* personX secretly loves java
```
]


---
.center[
![go on](img/goon.jpg)
]

???
Ask about Java experience.

---
.left-column[
## Comparison
### - pros
]
.right-column[
* types
* syntax
* data structures
* interfaces
* concurrency
* testing
* garbage collection
* memory management
]


---
.left-column[
## Comparison
### - pros
### - neutral
]
.right-column[
* types
* syntax
* data structures
* interfaces
* concurrency
* testing
* garbage collection
* memory management
<br /><br /><br />
* code organization
* error handling
]


---
.left-column[
## Comparison
### - pros
### - neutral
### - cons
]
.right-column[
* types
* syntax
* data structures
* interfaces
* concurrency
* testing
* garbage collection
* memory management
<br /><br /><br />
* code organization
* error handling
<br /><br /><br />
* dependencies management
* debugger
]

---
.left-column[
## Comparison
]
.right-column[
```java
public class HelloWorld {
    public static void main(String[] args) {
        System.out.println("Hello, World");
    }
}
```
```bash
$ javac main.java
$ java Main
```
]


--
.right-column[
```go
package main

import "fmt"

func main() {
    fmt.Println("Hello world!")
}
```
```bash
$ go run main.go
```
]


---
.left-column[
## Why
]
.right-column[
*No major systems language has emerged in over a decade, but over that time the computing landscape has changed tremendously.*
]

--
.right-column[
Robert Griesemer, Rob Pike and Ken Thompson:

* fast development

* fast compilation

* no type hierarchy

* good GC & concurrency

* multi-core machines
]

???
- Increase the time need to develop new systems, to allow meeting current
demands of market;.
- Developer expects fast compilation times.
- Go's type system has no hierarchy, and although it has static types
the language attempts to make types feel lighter weight than, for example Java
or other OO languages.
- Go is fully garbage-collected and provides improved support for concurrent
execution and communication.


---
.left-column[
## Comparison
### - types
]
.right-column[
```go
var age int = 35
```
```go
var age int
age = 35
```
```go
age := 35
_ = age
```
```go
var myArray [1]string
var myMap map[string]string
```
]

???
Types: boolean, numeric, string, array and maps.

Implicit conversion between types, even those predefined is not possible, iow.
there's no possibility to implicitly convert int16 to int32.

Unused variables are compilation error, the same applies to unused imports.

No type definition in short variable declaration syntax.
There's one caveat with short variable declaration syntax, it's so handy that it's
sometimes overused, leading to shadowing variables.


---
.left-column[
## Comparison
### - types
]
.right-column[
```go
type ByteSize float64

const (
    _           = iota
    KB ByteSize = 1 << (10 * iota)
    MB
    GB
    TB
)
```
```go
var myArray [3]string
myArray[0] = "one"
myArray[1] = "two"
myArray[2] = "three"
```
```go
var slice []string = myArray[1:3]
// -> {"two", "three"}
```
]

???
With iota it's super easy to create enumerated types.

As mentioned before, Go provides array similarly to Java. It is of fixed size,
although when working with them, the idioms available in the language let you
forget that fact.

It's the slices are where all the action in Go happens. A slice is a data
structure describing a contiguous section of an array stored separately from the
slice variable itself. A slice is not an array. A slice describes a piece of an
array. In the example we're creating a slice from first element inclusive through
3, exclusive.
One important difference is that Go passes function arguments as values, so if
you pass the array and the function modifies it, it won't be visible outside
the function unless you pass the address of the array or use the slice which
provides direct access to array's underlying data, even though you're again
passing copy of the slice.

---
.left-column[
## Comparison
### - types
### - syntax
]
.right-column[
```go
if x > 0 {
    return y
}
```
```go
if err := check(file); err != nil {
    return err
}
```
```go
if value, ok := myMap["key"]; !ok {
    return "not found"
}
```
]

???
No requirement for having parenthesis around conditions, even with multiple
conditions.
Go requires curly braces for conditions as well as loops, even single liners.
Use gofmt and forget about formatting.
Go-based projects require gofmt before submitting PRs.


---
.left-column[
## Comparison
### - types
### - syntax
]
.right-column[
```go
sum := 0
for i := 0; i < 10; i++ {
    sum += i
}
```
```go
for index, value := range myArray {
  fmt.Printf("%d: %s\n", index, value)
}
```
```go
for key, value := range myMap {
    fmt.Printf("%s: %s\n", key, value)
}
```
]

???
When iterating with for-each and you need to modify underlying data use
index instead since Go will pass the value not a pointer.

---
.left-column[
## Comparison
### - types
### - syntax
]
.right-column[
```go
switch method {
case "ping":
  err = decodePing(req)
case "push":
  err = decodePush(req)
default:
  err = errors.New("Unknown method!")
}
```
```go
switch {
case '0' <= c && c <= '9':
    return c - '0'
case 'a' <= c && c <= 'f':
    return c - 'a' + 10
case 'A' <= c && c <= 'F':
    return c - 'A' + 10
}
```
]

???
There's no automatic fall through like in Java, although such behavior can be
enforced with fallthrough keyword.


---
.left-column[
## Comparison
### - types
### - syntax
]
.right-column[
```go
switch t := t.(type) {
case bool:
    fmt.Printf("boolean %t\n", t)
case int:
    fmt.Printf("integer %d\n", t)
default:
    fmt.Printf("unexpected type %T\n", t)
}
```
]

???
Interesting construct - type switch, used to discover the dynamic type of an
interface variable. It uses type assertion construct.


---
.left-column[
## Comparison
### - types
### - syntax
]
.right-column[
```go
func List(s string) (Result, error) {
    if err := Get(s); err != nil {
        return nil, err
    }
    var res Result
    for k, v := range(list(s)) {
        res.Append(k, v)
    }
    return res
}
```
]

???
Multiple return values.

--
.right-column[
```go
func List(s string) (res Result, err error) {
    if err = Get(s); err != nil {
        return
    }
    for k, v := range(list(s)) {
        res.Append(k, v)
    }
    return
}
```
]

???
Named return values.


---
.left-column[
## Comparison
### - types
### - syntax
]
.right-column[
```go
List := func(s string) {Result, error) {
    // body goes here...
}
```
```go
file, err := os.Open(path)
if err != nil {
    return err
}
defer file.Close()
...
// do something with the file
...
```
]

???

Function literals, function types.

Go's defer statement schedules a function call to be run immediately before the
function executing the defer returns, regardless of which patch a function takes
to return.


---
.left-column[
## Comparison
### - types
### - syntax
### - data structures
]
.right-column[
```go
type MyStruct struct {
    Name  string
    Value string
}
```
```go
x := new(MyStruct)
var y MyStruct
```
```go
z := make(map[string]string)
```
]

???
new allocates memory, but it does not initialize the memory, it only zeros it,
and returns pointer to newly allocated memory. In the cases where more initialization
is needed use initialization method, unsurprisingly called New ;)

make creates slices, maps, and channels only, and it returns an initialized
(not zeroed) value of given type. They need special initialization.


---
.left-column[
## Comparison
### - types
### - syntax
### - data structures
### - interfaces
]
.right-column[

```go
type MyInterface interface {
    Set(string) error
}
```
]

--
.right-column[
```go
type MyStruct struct {
    Name  string
    Value string
}

func (m *MyStruct) Set(newValue string) error {
    if err := validate(newValue); err != nil {
        return err
    }
    m.Value = newValue
    return nil
}

func (m MyStruct) Get() string {
    return m.Value
}
```
]

???
Additionally there's no need to explicitly specify which interfaces
we satisfy, it's being done automatically at compile time.

Since interfaces are implicit, it is very common to have very narrow, specialized
interfaces with only one or two methods which are then implemented within single
structure.

Pointer receivers - can modify underlying data.
Value receivers - cannot modify underlying data.


---
.left-column[
## Comparison
### - types
### - syntax
### - data structures
### - interfaces
### - concurrency
]
.right-column[
*Do not communicate by sharing memory; instead, share memory by communicating.*
]

???
It is really hard and challenging to write properly functioning concurrent piece
of software. Most often you end up struggling with shared access to a variable.
Agreed? Go encourages a different approach, in which shared values are passed
around on channels and, in fact, never actively shared by separate threads of
execution. Only one goroutine has access to the value at any given time.
Data races cannot occur, by design. The slogan:

Goroutines is a new term, because the existing terms (threads, coroutines, processes,
and so on) does not reflect accurately what they are.
A goroutine is a function executing concurrently with other goroutines in the same
address space. It is lightweight, costing little more than the allocation of stack
space. And the stacks start small, so they are cheap, and grow by allocating (and
freeing) heap storage as required.

Goroutines are multiplexed onto multiple OS threads so if one should block, such
as while waiting for I/O, others continue to run. Their design hides many of the
complexities of thread creation and management.

Prefix a function or method call with the go keyword to run the call in a new goroutine.
When the call completes, the goroutine exits, silently. (The effect is similar to
the Unix shell's & notation for running a command in the background.)
One frequent mistake newcomers to Go make is, that the main program will not wait
for the goroutines to finish, but it will exit when it reaches the end. There
are a couple solutions to this problem, let me introduce you first the channels.

--
.right-column[
```go
go func () {
    time.Sleep(200)
    fmt.Println("Hello world!")
}()
```
]


---
.left-column[
## Comparison
### - types
### - syntax
### - data structures
### - interfaces
### - concurrency
]
.right-column[
```go
c1 := make(chan int)        // unbuffered channel
```
```go
c2 := make(chan int, 10)    // buffered channel
```
]

???
Like maps, channels are allocated with make, and the resulting value acts as a
reference to an underlying data structure. Channels can be either buffered, the
optional integer parameter specifies buffer size for the channel, or unbuffered.


---
.left-column[
## Comparison
### - types
### - syntax
### - data structures
### - interfaces
### - concurrency
]
.right-column[
```go
go func() {
    time.Sleep(200)
    fmt.Println("Hello world!")
}()
```
```go
c := make(chan int)      // create channel
go func() {
    time.Sleep(200)
    fmt.Println("Hello world!")
    c <- 1              // send a signal
}()
<-c                     // waiting for a signal
```
]


---
.left-column[
## Comparison
### - types
### - syntax
### - data structures
### - interfaces
### - concurrency
### - testing
]
.right-column[
```go
import "testing"

func TestMyStruct(t *testing.T) {
    s := MyStruct{}
    if err := s.Set("value"); err != nil {
        t.Errorf("Unexpected error: %v", err)
  }
}
```
]

???
Built-in testing package.


---
.left-column[
## Comparison
### - dependencies management
]
.right-column[.small-code[
```json
{
  "ImportPath": "github.com/openshift/origin",
  "GoVersion": "go1.4.2",
  "Packages": [
    "./..."
  ],
  "Deps": [
    ...
    {
      "ImportPath": "k8s.io/kubernetes/pkg/controller",
      "Comment": "v1.2.0-alpha.4-851-g4a65fa1",
      "Rev": "4a65fa1f35e98ae96785836d99bf4ec7712ab682"
    },
    {
      "ImportPath": "k8s.io/kubernetes/pkg/conversion",
      "Comment": "v1.2.0-alpha.4-851-g4a65fa1",
      "Rev": "4a65fa1f35e98ae96785836d99bf4ec7712ab682"
    },
    {
      "ImportPath": "k8s.io/kubernetes/pkg/credentialprovider",
      "Comment": "v1.2.0-alpha.4-851-g4a65fa1",
      "Rev": "4a65fa1f35e98ae96785836d99bf4ec7712ab682"
    },
    {
      "ImportPath": "k8s.io/kubernetes/pkg/fieldpath",
      "Comment": "v1.2.0-alpha.4-851-g4a65fa1",
      "Rev": "4a65fa1f35e98ae96785836d99bf4ec7712ab682"
    },
    {
      "ImportPath": "k8s.io/kubernetes/pkg/fields",
      "Comment": "v1.2.0-alpha.4-851-g4a65fa1",
      "Rev": "4a65fa1f35e98ae96785836d99bf4ec7712ab682"
    },
    {
      "ImportPath": "k8s.io/kubernetes/pkg/healthz",
      "Comment": "v1.2.0-alpha.4-851-g4a65fa1",
      "Rev": "4a65fa1f35e98ae96785836d99bf4ec7712ab682"
    },
    ...
  ]
}
```
]]

???
Almost 1600 lines in openshift origin server code.

---
.left-column[
## Comparison
### - dependencies management
### - debugger
]
.right-column[.small-code[
https://github.com/derekparker/delve
```bash
$ dlv exec oc annotate job/pi foo=bar

Type 'help' for list of commands.
(dlv) b annotate.go:121
Breakpoint 1 set at 0x4fa4d6 for k8s.io/kubernetes/pkg/kubectl/cmd...

(dlv) c
> k8s.io/kubernetes/pkg/kubectl/cmd.(*AnnotateOptions).Complete() ...

(dlv) print namespace
"test"

(dlv) locals
annotationArgs = []string len: 0, cap: 0, []
b·2 = *struct k8s.io/kubernetes/pkg/kubectl/resource.Builder nil
clientMapper·4 = (unreadable invalid interface type: clientMapper·4.tab...
enforceNamespace = false
mapper = (unreadable invalid interface type)
mapper·2 = (unreadable invalid interface type: mapper·2.tab._type is nil)
metAnnotaionArg = false
namespace = "test"
namespace·3 = (unreadable could not read string at 0x5 due to input/output ...
s = "\x0f�\\$ ��\x00\x0f�>����������k���\x11���\x00dH� ...
suffix·3 = "\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00 ...
typer = k8s.io/kubernetes/pkg/runtime.ObjectTyper (unreadable unknown or ...
typer·3 = (unreadable invalid interface type)

(dlv) n
> k8s.io/kubernetes/pkg/kubectl/cmd.(*AnnotateOptions). ... annotate.go:127

(dlv)
> k8s.io/kubernetes/pkg/kubectl/cmd.(*AnnotateOptions). ... annotate.go:128

(dlv) c
job "pi" annotated
```
]]

???
And although Derek Parker, the creator of delve is an awesome person it is
really hard to debug Go programs.


---
.left-column[
## Links
]
.right-column[
The Go Playground:<br />
http://play.golang.org/

Effective Go:<br />
https://golang.org/doc/effective_go.html

50 Shades of Go:<br />
http://devs.cloudimmunity.com/gotchas-and-common-mistakes-in-go-golang/
]
