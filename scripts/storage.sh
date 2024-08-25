#!/bin/bash

set -o allexport
. .env 
set +o allexport

# Create a storage account
az storage account create \
    --name $STORAGE_ACCOUNT_NAME\
    --resource-group $RESOURCE_GROUP_NAME\
    --location $LOCATION\
    --sku Standard_RAGRS\
    --kind StorageV2 \

    