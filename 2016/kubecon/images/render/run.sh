#!/bin/bash -e

pushd $HOME &> /dev/null

url=$1
source $HOME/.venv/bin/activate

if [ "${url:0:4}" == "amqp" ]; then
    for i in {1..5}; do
        itemurl=$(/bin/amqp-consume --url=${url} -q renderer -c 1 cat)
        #download and execute script
        wget --quiet -O $HOME/script.py ${itemurl}
        python $HOME/script.py
    done
else
    #download and execute script
    wget --quiet -O $HOME/script.py ${url}
    python $HOME/script.py
fi
