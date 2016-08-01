#!/bin/bash

echo "[INFO] Pre-pull necessary docker images..."
images="
    docker.io/centos/python-35-centos7:latest \
    docker.io/centos/ruby-23-centos7:latest \
    docker.io/centos/php-56-centos7:latest \
    docker.io/centos/perl-520-centos7:latest \
    docker.io/centos/nodejs-4-centos7:latest \ \
    docker.io/openshift/hello-openshift:latest \
    docker.io/openshift/origin-sti-builder:v1.3.0-alpha.2 \
    docker.io/openshift/origin-deployer:v1.3.0-alpha.2 \
    docker.io/openshift/origin-docker-registry:v1.3.0-alpha.2 \
    docker.io/openshift/origin-haproxy-router:v1.3.0-alpha.2 \
    docker.io/openshift/origin:v1.3.0-alpha.2 \
    docker.io/openshift/origin-pod:v1.3.0-alpha.2"
for img in $images; do
    docker pull $img
done

echo "[INFO] Check if oc cluster up/down works..."
oc cluster up
while true; do
    curl --max-time 2 -kfs https://10.2.2.2:8443/healthz &>/dev/null
    if [[ $? -eq 0 ]]; then
        break
    fi
    sleep 1
done
oc cluster down

echo "[INFO] Compacting disk..."
sudo dd if=/dev/zero of=/EMPTY bs=1M
sudo rm -f /EMPTY
sync

echo "[INFO] Clear history..."
cat /dev/null > ~/.bash_history && history -c && exit
