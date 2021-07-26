#! /bin/bash
pushd $(dirname $0)

# stop glances
pkill glances

# stop testinfra
pkill -f server.py

# stop docker server
pushd ./Docker
docker-compose down
popd

popd
