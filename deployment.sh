#!/bin/bash

# Parameters:
# $1 - name of the directory in which target source code is located (without ./)
# $2 - old prefix of Docker images and containers (which will be removed)
# $3 - new prefix of Docker images and containers (which will be created)
#    - if absent, $2 is used

if [ $# -lt 2 -o $# -gt 3 ]
then
  echo "Illegal number of parameters."
  exit 0
fi

if [ $# -eq 3 ]
then
  prefix=$3
else
  prefix=$2
fi

docker rm -f `docker ps -aq -f name="$2-*"`
docker rmi -f `docker images -aq "$2-*"`

if [ -z `docker images -aq "my-python"` ]
then
  docker build . -f ./common/my-python.dockerfile -t my-python --no-cache
fi

for img in `find "./$1/deployment" -name "*.dockerfile"`
do
  name=`echo $img | sed "s:^.*\/\([a-z|-]*\)\.dockerfile:$prefix-\1-img:"`
  docker build -f "$img" -t "$name" --no-cache .
done

docker network rm "$2-$1-net"
docker network create "$prefix-$1-net"

export PREFIX=$prefix
docker-compose -f "./$1/deployment/docker-compose.yaml" up --detach
