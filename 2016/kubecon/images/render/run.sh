#!/bin/bash -e

pushd $HOME &> /dev/null

url=$1
if [ "${url:0:4}" == "amqp" ]; then
    for i in {1..5}; do
        newurl=$(/bin/amqp-consume --url=${url} -q renderer -c 1 cat)
        url=${newurl}
        #download and execute script
        wget --quiet -O $HOME/script.py ${url}
        source $HOME/.venv/bin/activate
        exec python $HOME/script.py
    done
else
    #download and execute script
    wget --quiet -O $HOME/script.py ${url}
    source $HOME/.venv/bin/activate
    exec python $HOME/script.py
fi
