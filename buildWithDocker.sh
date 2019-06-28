#!/bin/bash


docker rm -f evaluationlinks
docker rmi evaluationlinks
docker build -t evaluationlinks .
