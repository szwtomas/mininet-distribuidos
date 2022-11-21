# Mininet - Distribuidos

## Prerequisites

For running this project, you should have **Docker** and **Docker Compose** installed on your computer.

Follow installation instructions on [the official Docker documentation](https://docs.docker.com/engine/install/ubuntu/).

The idea behind using Docker for this project is to make dependencies management as simple as possible, considering mininet only runs on Linux environments.

## Dockerfile and docker-compose.yml

The Dockerfile has instructions on how to build the Docker image. In this case, we are using Ubuntu 18 and installing mininet among other depedencies inside the container.

The docker-compose.yml file also has instructions on how to run the container, and how to configure volumes so that scripts and python files with our code are copied inside the container

## Running the container and scripts

### On Linux

First, make sure you have all the requisites installed.

Then, run the following command: `./run.sh -l`. The -l flag is to indicate you are using linux. If you have permission errors, run the command

`chmod +x ./run.sh` and try again.

This will prompt you a bash command line inside the contaiener, where you have to run pox. For this, run the following command:

`./pox/pox.py`

Or whatever pox command you want to use. This will make pox listen, but we still have to run mininet. To do this, open a new tab, go to the root repository directory and run the following script:

`sudo ./connect-container.sh`

This will connect via **ssh** to the existing container that has pox listening. Inside the container, run:

`./scripts/runLinear.sh`

### On Mac OS

First, make sure you have all the requisites installed.

Then, run the following command: `./run.sh`. If you have permission errors, run the command

`chmod +x ./run.sh` and try again.

This will prompt you a bash command line inside the contaiener, where you have to run pox. For this, run the following command:

`./pox/pox.py`

Or whatever pox command you want to use. This will make pox listen, but we still have to run mininet. To do this, open a new tab, go to the root repository directory and run the following script:

`./connect-container.sh`

This will connect via **ssh** to the existing container that has pox listening. Inside the container, run:

`./scripts/runLinear.sh`

### On windows

First, make sure you have all the requisites installed. Then, stop using windows and install linux, and follow the linux instructions.


## Firewall Rules:

1) dst port 80

2) src host 1, dst port 5001, protocol UDP

3) having selected for example host 1 and host 2: src host 1 and dst host 2, or src host 2 and dst host 1