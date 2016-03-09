#!/bin/bash -e

echo "Setting up data..."
sudo mkdir -p /tmp/data
sudo chmod 777 /tmp/data

mkdir -p tmp
python3 generate.py
pushd tmp
python3 -m http.server 1111 &>/dev/null &
popd

echo "Setting up rabbitmq..."
kubectl create -f rabbitmq.yaml
set +e
while true; do
    kubectl get pods | grep rabbitmq | grep Running
    if [ $? -eq 0 ]; then
        break
    fi
    sleep 1
done
sleep 3
set -e

broker_ip=$(kubectl get svc/rabbitmq-service --template '{{.spec.clusterIP}}')
broker_url=amqp://guest:guest@$broker_ip:5672
amqp-declare-queue --url=${broker_url} -q renderer -d
for i in {1..40}; do
    amqp-publish --url=${broker_url} -r renderer -p -b "http://192.168.121.118:1111/$(printf %02d.py $i)"
done
sleep 3

echo "Setting up the job..."
sed 's|BROKER_URL|'${broker_url}'|g' render.yaml > render.yaml.tmp
kubectl create -f render.yaml.tmp
rm render.yaml.tmp

pushd /tmp/data
python3 -m http.server 2222 &>/dev/null &
