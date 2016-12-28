#!/usr/bin/env bash
# clean env
echo "Clean env..."
docker-compose -f test/docker-compose-test.yml stop
docker-compose -f test/docker-compose-test.yml kill
docker-compose -f test/docker-compose-test.yml rm -f

# start env and wait until services started
echo "Setup env..."
docker pull tcz001/hyperledger-fabric-cop
docker pull tcz001/hyperledger-fabric-peer
docker pull tcz001/hyperledger-fabric-orderer
docker tag tcz001/hyperledger-fabric-cop:latest hyperledger/fabric-cop:latest
docker tag tcz001/hyperledger-fabric-peer:latest hyperledger/fabric-peer:latest
docker tag tcz001/hyperledger-fabric-orderer:latest hyperledger/fabric-order:latest

docker-compose -f test/docker-compose-test.yml up &

sleep 10

# run tests
echo "Starting test..."
docker exec -it fabric-sdk-py make test

# clean env
docker-compose -f test/docker-compose-test.yml stop
docker-compose -f test/docker-compose-test.yml kill
docker-compose -f test/docker-compose-test.yml rm -f