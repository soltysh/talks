#!/bin/bash -e

if [ "$#" == "0" ]; then
    echo "Pass broker IP!"
    return 1
fi

broker_url=amqp://guest:guest@$1:5672
amqp-declare-queue --url=${broker_url} -q renderer -d
amqp-publish --url=${broker_url} -r renderer -p -b "http://172.17.0.1:8000/vapory.py"
