#!/bin/sh

#export FLASK_ENV=development
export FLASK_APP=./evaluationSameAs/index.py

#source $(pipenv --venv)/bin/activate
flask run -h 0.0.0.0 -p 5000
