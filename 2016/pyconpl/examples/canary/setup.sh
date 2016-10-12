#!/bin/bash
oc new-project canary
# prod deployment
oc create -f prod.yaml
oc expose dc/prod --port 8080
oc expose svc/prod --name=prod
# canary deployment
oc create -f canary.yaml
oc expose dc/canary --port 8080
oc set route-backends prod prod=100 canary=0
