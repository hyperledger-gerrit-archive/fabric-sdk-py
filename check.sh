#!/bin/bash

# checking local version
echo "===Checking Docker and Docker-Compose version"
docker version
docker-compose -v

# pull fabric images
echo "===Pulling fabric images..."
docker pull yeasy/hyperledger-fabric-cop
docker pull yeasy/hyperledger-fabric-peer
docker pull yeasy/hyperledger-fabric-orderer
docker tag yeasy/hyperledger-fabric-cop:latest hyperledger/fabric-cop:latest
docker tag yeasy/hyperledger-fabric-peer:latest hyperledger/fabric-peer:latest
docker tag yeasy/hyperledger-fabric-orderer:latest hyperledger/fabric-order:latest

# run tests
echo "===Starting test..."
make unittest