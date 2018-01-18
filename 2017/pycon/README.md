Effectively running python applications in Kubernetes/OpenShift
---------------------------------------------------------------

You can easily deploy the workshop materials using one of the following commands.

    docker run -ti \
        -v `pwd`:/app-data \
        -p 8080:8080 \
        -e CONTENT_URL_PREFIX="file:///app-data" \
        -e WORKSHOPS_URLS="file:///app-data/_workshop.yml" \
        docker.io/osevg/workshopper

This will run a local docker image containing the [workshopper instace](https://github.com/osevg/workshopper).
You should be able to access it at [http://localhost:8080/](http://localhost:8080).
Don't forget to add `:Z` to volume when SELinux is enabled.

Alternatively, you can deploy it in OpenShift using:

    oc new-app \
        docker.io/osevg/workshopper \
        -e WORKSHOPS_URLS=https://raw.githubusercontent.com/soltysh/talks/master/2017/pycon/_workshop.yml \
        --name pycon-tutorial

    oc expose svc/pycon-tutorial

