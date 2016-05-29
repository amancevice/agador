#!/bin/bash

TEAL='\033[1;38m'
NC='\033[0m'

echo "Building example client Docker image"
docker build -t amancevice/agador:example . > /dev/null

echo "Creating agador docker bridge network"
docker network create --driver bridge agador > /dev/null

echo "Starting influxdb"
docker run --detach --name influx \
    --hostname influx \
    --net agador \
    influxdb > /dev/null

echo "Starting dynamodb"
docker run --detach --name dynamodb \
    --hostname dynamodb \
    --net agador \
    ryanratcliff/dynamodb > /dev/null

echo "Starting agador with config:"
echo
printf "${TEAL}$(cat ./example.yaml)${NC}"
echo
docker run --detach --name agador \
    --volume $(pwd)/example.yaml:/home/agador/example.yaml \
    --hostname agador \
    --net agador \
    amancevice/agador --config /home/agador/example.yaml > /dev/null

echo
echo "Running example Python:"
echo
printf "${TEAL}$(cat ./example.py)${NC}"
echo
echo
printf "Output:\n\n${TEAL}"
docker run --rm --name example \
    --hostname example \
    --net agador \
    amancevice/agador:example
printf "${NC}"

echo
echo "Cleaning up"
docker rm -f influx dynamodb agador > /dev/null
docker rmi amancevice/agador:example > /dev/null
docker network rm agador > /dev/null
