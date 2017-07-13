#!/usr/bin/env bash

IMG_NAME=hyperledger/fabric-sdk-py
CONTAINER_NAME=fabric-sdk-py

if [[ "$(docker images -q $IMG_NAME 2> /dev/null)" == "" ]]; then
	echo "There's no $IMG_NAME image, build it first."
  cd ../
  docker build -t $IMG_NAME .
  cd -
fi

echo "Start up a fabric-ca container."
docker run \
  --name fabric-ca \
  -d -it \
	-v /tmp:/tmp \
	-v $GOPATH/src/github.com/hyperledger:/opt/go/src/github.com/hyperledger \
	yeasy/hyperledger-fabric bash -c 'while true; do sleep 1000; done'


echo "Start up a fabric-sdk-py container."
docker run \
  --name $CONTAINER_NAME \
  -d -it \
	-v /tmp:/tmp \
	-v $GOPATH/src/github.com/hyperledger/fabric-sdk-py:/fabric-sdk-py \
	$IMG_NAME


docker exec -it $CONTAINER_NAME bash
