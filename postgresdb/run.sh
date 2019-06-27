#!/bin/bash



docker rm -f postgresdb
docker run -d -p 5432:5432 --name  postgresdb -v dbvol:/var/lib/postgresql/data postgresgld

