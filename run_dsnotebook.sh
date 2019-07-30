#!/usr/bin/env bash

#EDIT THE FOLLOWING. CHANGE TO YOUR ORGS LICENSE_ID
image="mfreitas/ds_notebook_extra"
name="ds_notebook_extra"
tag="latest"
share=${PWD}

#EDIT THE FOLLOWING. CHANGE TO YOUR PREFERRED HTTP PORT
port=8888

echo "Stopping DS Notebook"
docker container stop $name
docker rm $name

docker login registry.gitlab.com
docker pull registry.gitlab.com/$docker_image:$tag

echo "Starting up DS Notebook"
docker run -d \
      -p $port:$port \
      -v "$share":"/data" \
      --name $name \
      registry.gitlab.com/$image:$tag  /bin/bash -c "jupyter notebook \
      --ip 0.0.0.0 --no-browser --allow-root --NotebookApp.token='' \
      --notebook-dir='/data'"

sleep 5

open http://localhost:$port

