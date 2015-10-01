#!/bin/bash

tmpjs=$(mktemp)
cat <<EOF > $tmpjs
db.video.insert({'title': 'openshift is sooo cool', 'url': 'http://www.example.com/cool'});
db.video.insert({'title': 'openshift is awesome', 'url': 'http://www.example.com/awesome'});
db.video.insert({'title': 'soltysh is very handsome', 'url': 'http://www.example.com/handsome'});
db.video.insert({'title': 'kittens are soo cute', 'url': 'http://www.example.com/cute'});
db.video.insert({'title': 'programming in python', 'url': 'http://www.python.org/'});
db.video.insert({'title': 'programming in go', 'url': 'http://www.golang.org/'});
EOF

mongo $1:$2/blast_text --username $3 --password $4 --authenticationDatabase blast_text $tmpjs

rm $tmpjs
