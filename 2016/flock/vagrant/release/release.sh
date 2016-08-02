#!/bin/bash

echo "[INFO] Spinning up the F23 base box..."
vagrant up

echo "[INFO] Setting up the devenv..."
vagrant ssh -c '/utils/setup1.sh'
vagrant ssh -c '/utils/setup2.sh'

echo "[INFO] Packaging the dev box..."
vagrant halt
vagrant package --base origin --output openshift3-origin.box --vagrantfile=release/Vagrantfile
