#!/bin/bash

set -o allexport
. .env 
set +o allexport

# Create a flexible postgres server in Azure
az postgres flexible-server create \
    --resource-group $RESOURCE_GROUP_NAME \
    --name $POSTGRES_SERVER_NAME \
    --location $LOCATION \
    --admin-user $POSTGRES_ADMIN_USER \
    --admin-password $POSTGRES_ADMIN_PASSWORD \
    --sku-name $POSTGRES_SKU \
    --tier Burstable \
    --storage-size $POSTGRES_SOTRAGE_SIZE \
    --storage-auto-grow Disabled \
    --geo-redundant-backup Disabled

# Create a firewall rule to allow IP address
az postgres flexible-server firewall-rule create \
    --resource-group $RESOURCE_GROUP_NAME \
    --name $POSTGRES_SERVER_NAME \
    --rule-name AllowPublicAccess \
    --start-ip-address 0.0.0.0 \
    --end-ip-address 255.255.255.255

# Retrieve the connection string
connection_string=$(az postgres flexible-server show \
    --resource-group $RESOURCE_GROUP_NAME \
    --name $POSTGRES_SERVER_NAME \
    --query "connectionStrings[0].connectionString" \
    --output tsv)

# Print the connection string
echo $connection_string

# Create a database
az postgres flexible-server db create \
    --resource-group $RESOURCE_GROUP_NAME \
    --server-name $POSTGRES_SERVER_NAME \
    --database-name $POSTGRES_DB_NAME


