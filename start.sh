#!/bin/bash

if [ -e .env ]; then
    source .env
else
    echo "Please set up your .env file before starting your enviornment."
    exit 1
fi

docker-compose -f .docker/docker-compose.yml up -d --build

exit 0
