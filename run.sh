#!/bin/bash -ex

docker build -t app .

docker run \
    -p 8000:8000 \
    --rm \
    app python -m app
