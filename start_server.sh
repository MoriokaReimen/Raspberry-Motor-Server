#! /bin/bash
pushd $(dirname $0)

# launch glances
printf "youkan" | glances -w --username --password --port 20000 1> /dev/null 2> /dev/null & disown

# launch testinfra
pushd ./testinfra
python3 server.py 1> /dev/null 2> /dev/null & disown
popd

# launch docker servers
pushd ./Docker
docker-compose up 1> /dev/null 2> /dev/null & disown
popd

popd

