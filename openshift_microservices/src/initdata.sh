#!/bin/bash
blast-image/initdata.sh $(oc get service/blast-image-db -t "{{.spec.clusterIP}}") 5432 \
    # this is very hack-ish - DON'T EVER DO THIS!!!
    $(oc get dc/blast-image-db -t "{{ (index (index .spec.template.spec.containers 0).env 0).value }}") \
    $(oc get dc/blast-image-db -t "{{ (index (index .spec.template.spec.containers 0).env 1).value }}")

blast-text/initdata.sh $(oc get service/blast-text-db -t "{{.spec.clusterIP}}") 27017 \
    # this is very hack-ish - DON'T EVER DO THIS!!!
    $(oc get dc/blast-text-db -t "{{ (index (index .spec.template.spec.containers 0).env 0).value }}") \
    $(oc get dc/blast-text-db -t "{{ (index (index .spec.template.spec.containers 0).env 1).value }}")

blast-video/initdata.sh $(oc get service/blast-video-db -t "{{.spec.clusterIP}}") 6379
