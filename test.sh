#!/bin/bash -ex

docker build -t app .

# create file for logs
rm -fr logs
mkdir -p logs
touch logs/service.log

docker run \
    -it \
    -p 6000:6000 \
    --rm \
    --workdir /test \
    -v ${PWD}/logs:/logs:rw \
    app pytest
