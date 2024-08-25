#!/bin/bash

set -o allexport
. .env 
set +o allexport


echo $RESOURCE_GROUP
echo $LOCATION
#create a new ressource group 
az group create --name $RESOURCE_GROUP_NAME --location $LOCATION