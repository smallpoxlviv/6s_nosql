#!/bin/bash

docker build -t nosql_app:latest .

docker run -v /temp:/app/resources -p 8081:8081 nosql_app
