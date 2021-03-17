#!/bin/bash

function usage(){
  filename=`basename -- $0`
  echo -e "\nmissing arguments\n"
  echo -e "usage:"
  echo -e "${filename} CLUSTER TARGET_TONIQ(i.e. data, app or all), ENVIRONMENT(i.e. internal, staging, prod)\n"
}

if [ $# -lt 2 ]
then
    usage
    exit -1
fi

MODULE_NAME=$(basename `git rev-parse --show-toplevel`)
VERSION_TAG=`cat VERSION | tr -d '\n'`
SHORT_UID=`uuidgen | cut -d '-' -f1 | tr "[:upper:]" "[:lower:]"`
CLUSTER=${1}
TARGET_TONIQ=${2}
ENVIRONMENT=${3}

# Module job or app can be deployed to different environments
VALUES_DIR=${ENVIRONMENT}-${TARGET_TONIQ}

current_context=`kubectx -c`
kubectx $CLUSTER

helm upgrade --wait --install \
  -f ./deployments/helm_vars/${VALUES_DIR}/values.yaml \
  --timeout 1800s \
  --namespace default \
  --set module_name=$MODULE_NAME \
  --set module_version=$VERSION_TAG \
  --set job.uid=$SHORT_UID \
  $MODULE_NAME ./deployments/helm/

kubectx ${current_context}