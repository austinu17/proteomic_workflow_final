#!/usr/bin/env bash
echo "Starting up OpenMS Docker"
rnd_id=$RANDOM

docker login registry.gitlab.com -u mfreitas -p aoeLHVW7XvyQ9VfjxHWm 
docker_version=pwiz_dev
docker_image=registry.gitlab.com/mfreitas/docker_openms
data=${PWD}

echo "Checking for $docker_image:$docker_version"

if [[ "$(docker images -q $docker_image:$docker_version 2> /dev/null)" == "" ]]; then
  echo "Image not found. Pulling from dockerhub"
  docker pull $docker_image:$docker_version
fi

docker kill pipeline_worker_$rnd_id
docker rm pipeline_worker_$rnd_id

docker run -it \
      -v "$data":"/data" \
    --name pipeline_worker_$rnd_id \
    $docker_image:$docker_version \
    /bin/bash 

echo "Cleaning UP!"
sleep 5
docker container stop pipeline_worker_$rnd_id
docker rm pipeline_worker_$rnd_id
