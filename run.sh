#!/usr/bin/env bash



if [ $1 == "-l" ]; then
    sudo docker compose run mininet
else
    docker-compose run mininet
fi
