# Mininet - Distribuidos

## Prerequisites

For running this proyect, you should have **Docker** and **Docker Compose** installed on your computer.

Follow installation instructions on `https://docs.docker.com/engine/install/ubuntu/`.

The idea behind using Docker for this project is to make dependencies management as simple as possible, considering mininet only runs on Linux environments.

## Dockerfile and docker-compose.yml

The Dockerfile has instructions on how to build the Docker image. In this case, we are using Ubuntu 18 and installing mininet among other depedencies inside the container.

The docker-compose.yml file also has instructions on how to run the container, and how to configure volumes so that scripts and python files with our code are copied inside the container

## Running the container

Once you have al prerequisites installed, just run

`docker-compose run mininet`

This will prompt you to a bash shell inside the container.
Once inside the container, you should find the `/topology` directory in the root directory (run `cd /`), and the `scripts` directory in the home directory (run `cd`).

## Running scripts

For running our custom topology, just run:

`./scripts/runLinear.sh`.

If a "permission denied" pops up, run the following command inside the scripts directory:

`chmod +x runLinear.sh`
