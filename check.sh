#!/usr/bin/env bash
# clean env
docker-compose -f test/docker-compose-test.yml stop
docker-compose -f test/docker-compose-test.yml kill
docker-compose -f test/docker-compose-test.yml rm -f

# start env and wait until services started
docker-compose -f test/docker-compose-test.yml up -d