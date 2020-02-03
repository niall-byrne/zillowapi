#!/bin/bash

pushd zillowapi || exit 127
./manage.py wait_for_db
./manage.py migrate
./manage.py runserver 0.0.0.0:8000
