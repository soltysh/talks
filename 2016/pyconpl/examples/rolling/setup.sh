#!/bin/bash
oc new-project rolling
# oc run hello --image=openshift/hello-openshift
oc create -f rolling.yaml
oc expose dc/hello --port 8080
oc expose svc/hello
