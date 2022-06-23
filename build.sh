#!/bin/bash

docker stop nosql_container
docker rm nosql_container
docker rmi nosql_image

docker build -t nosql_image:latest .
