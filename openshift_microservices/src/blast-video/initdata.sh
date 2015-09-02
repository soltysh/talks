#!/bin/bash

tmplua=$(mktemp)
cat <<EOF > $tmplua
redis.call('rpush', 'openshift', 'https://youtu.be/FAJsx1HxsuM?t=2279')
redis.call('rpush', 'openshift', 'https://youtu.be/uocucZqg_0I')
redis.call('rpush', 'openshift', 'https://youtu.be/nDg8NuchvAs')
redis.call('rpush', 'pyconpl', 'https://youtu.be/T-ddE-aIX0k')
redis.call('rpush', 'pyconpl', 'https://youtu.be/CNvjKrCbw2A')
redis.call('rpush', 'pyconpl', 'https://youtu.be/-PisXGVe-lE')
EOF

redis-cli -h $1 -p $2 --eval $tmplua

rm $tmplua
