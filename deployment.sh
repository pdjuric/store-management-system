#!/bin/bash

to_kill=$(docker ps --filter=name=store- -q)
if [ -n "$to_kill" ]
then
  docker kill "$to_kill"
fi

to_rm=$(docker ps -a --filter=name=store- -q)
if [ -n "$to_rm" ]
then
  docker rmi "$to_rm"
fi


to_rmi=$( echo $(docker images "store-*" -a -q))
if [ -n "$to_rmi" ]
then
  docker rmi $to_rmi
fi

#docker system prune -a
#docker builder prune

old=$PWD
cd ..
if [ -z $(docker images "my-python" -a -q) ]
then
  docker build . -f ./common/my-python.dockerfile -t my-python --no-cache
fi

for img_file in $(find ./app-deploy -name "*.dockerfile" -maxdepth 2):
do
  img_name=$(echo $img_file | sed 's:^\.\/[a-z|-]*\/\([a-z|-]*\).*$:store-\1-img:')
  echo $PWD
  echo "docker build . -f $img_file -t $img_name --no-cache"
done

cd $old

docker network rm store-app-net
docker network create store-app-net

docker-compose -f app.yaml up --detach



