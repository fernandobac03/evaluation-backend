#!/bin/bash


docker rm -f postgresdb
docker rmi postgresgld
docker build -t postgresgld .

