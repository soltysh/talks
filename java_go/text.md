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

   * General Syntax

   * Types & Data Structures

   * Interfaces and OOP

   * Concurrency

   * Garbage Collection & Memory Management

   * Reflection

   * Web development

1. Summary
]


---
.left-column[
## @soltysh
]
.right-column[
## .awesome[.fa-twitter[] .fa-github[] .fa-google[] .fa-bitbucket[]]

### +10 years of experience
### C/C++ , Java , Go, Python
### dev -> team lead
### OpenShift
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
> there's plenty i miss about the JVM
```
]

--
.right-column[
```
> i miss it
> there's plenty i miss about the JVM
* engineer secretly loves java
```
]


---
.left-column[
## Comparison
### - pros
]
.right-column[
* syntax
* types & data structures
* interfaces and OOP
* concurrency
* garbage collection & memory management
* reflection
* web development
]


---
.left-column[
## Comparison
### - pros
### - neutral
]
.right-column[
* syntax
* types & data structures
* interfaces and OOP
* concurrency
* error handling
* reflection
* web development
* garbage collection & memory management
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
* syntax
* types & data structures
* interfaces and OOP
* concurrency
* error handling
* reflection
* web development
* garbage collection & memory management
<br /><br /><br />
* code organization
* error handling
<br /><br /><br />
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
var myArray []string
var myMap map[string]string
```
]

???
Go provides usually expected types, such as: boolean, numeric, string, array and
maps. As a complementary to arrays there are also slices. A slice is a descriptor
for a contiguous segment of an underlying array and provides access to a numbered
sequence of elements from that array. Additionally go provides struct types allowing
to define a sequence of fields, function types and an interface.

Although language is statically types is does not require, like other statically
types languages, to always define the type of a variable. The type can be
determined at runtime upon assignment.

Implicit conversion between types, even those predefined is not possible, iow.
there's no possibility to implicitly convert int16 to int32.

Unused variables are compilation error, the same applies to unused imports.

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
]

???
With iota it's super easy to create enumerated types.

Arrays, Slices!!! append

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
]


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
Iterating with foreach.
No while, do-while.


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
enforced with fallthrough key word.


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
Interesting construct - type switch.


---
.left-column[
## Comparison
### - types
### - syntax
### - data structures
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
One of Go's coolest features, which I've been dying to see in Java, is that functions
and methods can return multiple values.

The return "parameters" of a Go function can be given names and used as regular
variables, just like the incoming ones. When named, they are initialized to the
zero values for their types when the function begins; if the function executes
a return statement with no arguments, the current values of the result parameters
are used as the returned values.

This idiom is very frequently used to signal errors, ok etc. See opening file,
getting element from map.


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
Go has two allocation primitives, the built-in functions new and make. new allocates
memory, but it does not initialize the memory, it only zeros it, and returns pointer
to newly allocated memory.
Since the memory returned by new is zeroed, it's helpful to arrange your data
structures that the zero value of each type can be used without further initialization.
This means a user of the data structure can create one with new and get right to work.
Unfortunately this isn't always true, in those cases a method for initializing structure
is the recommended approach.

Since I've mentioned memory allocation, let's quickly jump to the other function
I've mentioned - make. It creates slices, maps, and channels only, and it returns
an initialized (not zeroed) value of type T. The reason for the distinction is
that these three types represent, under the covers, references to data structures
that must be initialized before use.


---
.left-column[
## Comparison
### - types
### - syntax
### - data structures
]
.right-column[
```go
type MyInterface interface {
    Set(string) error
}
```
]

???
Interfaces in Go, unlike in Java, provide a way to specify only the behavior of
an object. Additionally there's no need to explicitly specify which interfaces
we satisfy, it's being done automatically at compile time.

Since interfaces are implicit, it is very common to have very narrow, specialized
interfaces with only one or two methods which are then implemented within single
structure.


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
Speaking of implementation.
Difference between pointer vs. value receivers.


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
]

???
channels
goroutines


---
.left-column[
## Comparison
### - types
### - syntax
### - data structures
### - interfaces
### - concurrency
### - gc & memory
]
.right-column[
]


---
.left-column[
## Links
]
.right-column[
Effective Go:<br />
https://golang.org/doc/effective_go.html


50 Shades of Go:<br />
http://devs.cloudimmunity.com/gotchas-and-common-mistakes-in-go-golang/
]
