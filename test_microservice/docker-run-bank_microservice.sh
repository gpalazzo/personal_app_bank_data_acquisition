#!/usr/bin/env bash

sudo service docker start

docker build -t my_env_var_test .

docker run -e teste my_env_var_test
