#!/bin/bash

set -o allexport
. .env 
set +o allexport

# Delete the resources group
az group delete --name $RESOURCE_GROUP_NAME --yes