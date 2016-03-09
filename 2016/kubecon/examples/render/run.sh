#!/bin/bash -e

sudo mkdir -p /tmp/data
sudo chmod 777 /tmp/data
kubectl create -f render.yaml
