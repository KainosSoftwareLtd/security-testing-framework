#!/bin/bash

WORKING_DIR=$1
SOURCE_DIR=$2

docker run --env-file $WORKING_DIR/environment_variables_docker.env -t --rm=true -v $WORKING_DIR:/working -v $SOURCE_DIR:/source -w /working security-testing-framework $@ --rmm
