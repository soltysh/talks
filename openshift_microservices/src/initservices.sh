#!/bin/bash

for dir in $(find blast-* -maxdepth 0 -type d);
do
    oc new-app $dir/template.yaml
done
