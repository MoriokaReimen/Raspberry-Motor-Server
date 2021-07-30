#! /bin/bash
pushd $(dirname ${BASH_SOURCE}) 1> /dev/null

# launch glances
printf "youkan" | glances -w --username --password --port 20000 1> /dev/null 2> /dev/null & disown

# launch testinfra
pushd ./testinfra 1> /dev/null
python3 server.py 1> /dev/null 2> /dev/null & disown
popd 1> /dev/null

# launch docker servers
pushd ./Docker 1> /dev/null

# set up data directories if not exist
mkdir -p "./Gitea/gitea-data/"
mkdir -p "./GiteaDB/giteadb-data/"
mkdir -p "./Docker/Jenkins/jenkins_home/"

docker-compose up -d & disown
popd 1> /dev/null

popd 1> /dev/null

