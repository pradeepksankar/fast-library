#!/bin/bash

docker build -t app --target app .

#docker run --rm -it -p 8000:8000 app 

docker run -v "$PWD/fast-library.db:/app/fast-library.db" -p 8000:8000 fast-library

