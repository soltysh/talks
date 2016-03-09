#!/bin/bash -e

kubectl create -f rabbitmq.yaml
while true; do
    kubectl get pods|grep rabbitmq|grep Running
    if [ $? -eq 0 ]; then
        break
    fi
    sleep 1
done

broker_ip=$(kubectl get svc/rabbitmq-service --template '{{.spec.clusterIP}}')
broker_url=amqp://guest:guest@$broker_ip:5672
amqp-declare-queue --url=${broker_url} -q renderer -d
for i in {1..40}; do
    amqp-publish --url=${broker_url} -r renderer -p -b "http://192.168.121.118:8000/$(printf %02d.py $i)"
done

sed -i 's/BROKER_URL/${broker_url}/g' render.yaml
kubectl create -f render.yaml
