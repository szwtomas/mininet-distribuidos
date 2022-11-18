#!/bin/bash

CONTAINERNAME=$(docker ps --format "{{.Names}}" | grep mininet)

docker exec -it $CONTAINERNAME /bin/bash
