#!/bin/bash

docker build -t nosql_app:latest .

docker run -v /temp:/app/resources nosql_app
