#! /bin/bash
pushd $(dirname $0) 1> /dev/null

# stop glances
pkill glances

# stop testinfra
pkill -f server.py

# stop docker server
pushd ./Docker 1> /dev/null
docker-compose down
popd 1> /dev/null

popd 1> /dev/null
