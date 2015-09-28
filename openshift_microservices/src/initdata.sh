#!/bin/bash
blast-image/initdata.sh $(oc get service/blast-image -t "{{.spec.clusterIP}})" 8080 \
    # this is very hack-ish - DON'T EVER DO THIS!!!
    $(oc get dc/blast-image -t "{{ (index (index .spec.template.spec.containers 0).env 0).value }}") \
    $(oc get dc/blast-image -t "{{(index (index .spec.template.spec.containers 0).env 1).value}}")
