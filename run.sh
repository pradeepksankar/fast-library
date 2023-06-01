#!/bin/bash -ex

docker build -t app .

docker run \
    -it \
    -p 6000:6000 \
    --rm \
    app python -m app
