
#!/bin/bash

set -o allexport
. .env 
set +o allexport


# # retrieve the registry name
registry_name=$(az acr show --name $ACR_NAME --query loginServer --output tsv)

# # retrieve the registry access key
registry_password=$(az acr credential show --name $ACR_NAME --query "passwords[0].value" --output tsv)


# Verify the image exists in the registry
image_exists=$(az acr repository show --name $ACR_NAME --repository $DOCKER_IMAGE_API --output tsv)
if [ -z "$image_exists" ]; then
  echo "Error: Image '$ACR_NAME.azurecr.io/$DOCKER_IMAGE_API' does not exist in the registry."
  exit 1
fi


# # Create ACI container instance for the API
az container create \
  --resource-group $RESOURCE_GROUP_NAME \
  --name $API_ACI_NAME \
  --image $ACR_NAME.azurecr.io/$DOCKER_IMAGE_API \
  --registry-password $registry_password \
  --registry-login-server $ACR_NAME.azurecr.io \
  --registry-username $ACR_NAME \
  --dns-name-label $API_ACI_NAME \
  --ports 8000


# Verify the image exists in the registry
image_exists=$(az acr repository show --name $ACR_NAME --repository $DOCKER_IMAGE_SCRAPER --output tsv)
if [ -z "$image_exists" ]; then
  echo "Error: Image '$ACR_NAME.azurecr.io/$DOCKER_IMAGE_SCRAPER' does not exist in the registry."
  exit 1
fi


# Create ACI container instance scraper
az container create \
  --resource-group $RESOURCE_GROUP_NAME \
  --name $SCRAPER_ACI_NAME \
  --image $ACR_NAME.azurecr.io/$DOCKER_IMAGE_SCRAPER \
  --registry-password $registry_password \
  --registry-login-server $ACR_NAME.azurecr.io \
  --registry-username $ACR_NAME \
  --dns-name-label $SCRAPER_ACI_NAME


# Verify the image exists in the registry
image_exists=$(az acr repository show --name $ACR_NAME --repository $DOCKER_IMAGE_DASHBOARD --output tsv)
if [ -z "$image_exists" ]; then
  echo "Error: Image '$ACR_NAME.azurecr.io/$DOCKER_IMAGE_DASHBOARD' does not exist in the registry."
  exit 1
fi


# Create ACI container instance dashboard
az container create \
  --resource-group $RESOURCE_GROUP_NAME \
  --name $DASHBOARD_ACI_NAME \
  --image $ACR_NAME.azurecr.io/$DOCKER_IMAGE_DASHBOARD \
  --registry-password $registry_password \
  --registry-login-server $ACR_NAME.azurecr.io \
  --registry-username $ACR_NAME \
  --dns-name-label $DASHBOARD_ACI_NAME



# Get the storage account key
STORAGE_ACCOUNT_KEY=$(az storage account keys list --resource-group $RESOURCE_GROUP_NAME --account-name $STORAGE_ACCOUNT_NAME --query '[0].value' --output tsv)


# Verify the image exists in the registry
image_exists=$(az acr repository show --name $ACR_NAME --repository $DOCKER_IMAGE_TRAITMENT_MCF --output tsv)
if [ -z "$image_exists" ]; then
  echo "Error: Image '$ACR_NAME.azurecr.io/$DOCKER_IMAGE_TRAITMENT_MCF' does not exist in the registry."
  exit 1
fi


# Create ACI container instance traitement
az container create \
  --resource-group $RESOURCE_GROUP_NAME \
  --name $TRAITEMENT_ACI_NAME \
  --image $ACR_NAME.azurecr.io/$DOCKER_IMAGE_TRAITMENT_MCF \
  --registry-password $registry_password \
  --registry-login-server $ACR_NAME.azurecr.io \
  --registry-username $ACR_NAME \
  --dns-name-label $TRAITEMENT_ACI_NAME \
  --azure-file-volume-account-name $STORAGE_ACCOUNT_NAME \
  --azure-file-volume-account-key $STORAGE_ACCOUNT_KEY \
  --azure-file-volume-share-name $FILE_SHARE_NAME \
  --azure-file-volume-mount-path $MOUNT_PATH