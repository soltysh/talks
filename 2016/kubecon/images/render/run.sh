#!/bin/bash -e

pushd $HOME &> /dev/null

url=$1
if [ "${url:0:4}" == "amqp" ]; then
    newurl=$(/bin/amqp-consume --url=${url} -q renderer -c 1 cat)
    url=${newurl}
fi

#download and execute script
wget --quiet -O $HOME/script.py ${url}
source $HOME/.venv/bin/activate
exec python $HOME/script.py
