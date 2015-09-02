#!/bin/bash

tmpjs=$(mktemp)
cat <<EOF > $tmpjs
db.text.insert({'text': 'openshift is sooo cool', 'url': 'http://www.example.com/cool'});
db.text.insert({'text': 'openshift is awesome', 'url': 'http://www.example.com/awesome'});
db.text.insert({'text': 'soltysh is very handsome', 'url': 'http://www.example.com/handsome'});
db.text.insert({'text': 'kittens are soo cute', 'url': 'http://www.example.com/cute'});
db.text.insert({'text': 'programming in python', 'url': 'http://www.python.org/'});
db.text.insert({'text': 'programming in go', 'url': 'http://www.golang.org/'});
EOF

mongo $1:$2/blast_text --username $3 --password $4 --authenticationDatabase blast_text $tmpjs

rm $tmpjs
