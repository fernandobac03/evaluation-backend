#!/bin/bash



docker rm -f postgresdb
docker run -d -p 8080:5432 --name  postgresdb -v /home/mineria/volumesdocker/pgdb:/var/lib/postgresql/data postgresgld

