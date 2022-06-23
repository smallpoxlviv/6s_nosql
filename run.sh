#!/bin/bash

docker stop nosql_container
docker run --name nosql_container -v /temp:/app/resources -p 8081:8081 nosql_image
