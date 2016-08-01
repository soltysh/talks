#!/bin/bash

echo "[INFO] Upgrading system..."
sudo dnf upgrade -y

echo "[INFO] Installing dev tools..."
sudo dnf copr enable -y jcajka/golang1.6
sudo dnf install -y git golang-1.6.3 make docker

echo "[INFO] Setup insecure ssh keys..."
curl -s https://raw.githubusercontent.com/mitchellh/vagrant/master/keys/vagrant.pub > /home/vagrant/.ssh/authorized_keys
chmod 700 /home/vagrant/.ssh
chmod 600 /home/vagrant/.ssh/authorized_keys
chown -R vagrant:vagrant /home/vagrant/.ssh

echo "[INFO] Configure docker..."
echo "docker:x:1002:vagrant" | sudo tee --append /etc/group
echo "INSECURE_REGISTRY='--insecure-registry=172.30.0.0/16'" | sudo tee --append /etc/sysconfig/docker

sudo systemctl enable docker
sudo systemctl start docker

echo "[INFO] Setup origin devenv..."
mkdir -p /home/vagrant/go/src/github.com/openshift/
echo "export GOPATH=\$HOME/go" >> /home/vagrant/.bashrc
cd /home/vagrant/go/src/github.com/openshift/
git clone https://github.com/openshift/origin/

echo "[INFO] Compile origin master..."
export GOPATH=$HOME/go
cd origin/
make clean all

echo "[INFO] Install origin..."
sudo cp contrib/completions/bash/o* /etc/bash_completion.d/
mkdir -p /home/vagrant/bin
cp _output/local/bin/linux/amd64/* /home/vagrant/bin

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
