#!/bin/bash

# Also cloud buildo

BASE_GCR=us.gcr.io/terraform-254700/amplified
MODULE_PATH=`git rev-parse --show-toplevel`
MODULE_NAME=`basename $MODULE_PATH`
VERSION_TAG=`cat VERSION | tr -d '\n'`

cd $MODULE_PATH

docker build \
  -t $BASE_GCR/$MODULE_NAME:$VERSION_TAG -f ./build/docker/Dockerfile .

docker push $BASE_GCR/$MODULE_NAME:$VERSION_TAG