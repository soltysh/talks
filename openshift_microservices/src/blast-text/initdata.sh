#!/bin/bash

tmpjs=$(mktemp)
cat <<EOF > $tmpjs
db.text.insert({'text': 'openshift is sooo cool'});
db.text.insert({'text': 'openshift is awesome'});
db.text.insert({'text': 'soltysh is very handsome'});
db.text.insert({'text': 'kittens are soo cute'});
db.text.insert({'text': 'programming in python'});
db.text.insert({'text': 'programming in go'});
EOF

mongo $1:$2/blast_text --username $3 --password $4 --authenticationDatabase blast_text $tmpjs

rm $tmpjs
