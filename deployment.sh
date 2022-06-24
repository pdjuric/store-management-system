#!/bin/bash

# Parameters:
# $1 - name of the directory in which target source code is located (without ./)

if [ $# -ne 1 ]; then
  echo "Illegal number of parameters."
  exit 0
fi

# container and image cleanup
docker rm -f `docker ps -aq -f name="$1-*"` 2>/dev/null
docker rmi -f `docker images -aq "$1-*"` 2>/dev/null

# my-python image build
if [ -z `docker images -aq "my-python"` ]; then
  docker build . -f ./common/my-python.dockerfile -t my-python --no-cache
fi

for img in `find "./$1/deployment" -name "*.dockerfile"`; do

  # image build
  name=`echo $img | sed "s:^.*\/\([a-z|-]*\)\.dockerfile:\1:"`
  docker build -f "$img" -t "$1-$name" --no-cache .

  # network cleaup and build
  docker network rm "$1-$name-net"
  docker network create "$1-$name-net"

done

# volume cleanup and build
docker volume rm "$1-data"
docker volume create "$1-data"

# container build and deployment
docker-compose -f "./$1/deployment/docker-compose.yaml" up --detach

echo "Waiting for initial migrations  ..."
docker wait "$1-db-init" >/dev/null