#!/bin/bash
oc new-project blue-green
# blue deployment
oc create -f blue.yaml
oc expose dc/blue --port 8080
oc expose svc/blue --name=hello
# green deployment
oc create -f green.yaml
oc expose dc/green --port 8080
oc set route-backends hello blue=100 green=0
