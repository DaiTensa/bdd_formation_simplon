
#!/bin/bash

set -o allexport
. .env 
set +o allexport


az acr create --name $ACR_NAME --resource-group $RESOURCE_GROUP_NAME --sku standard --admin-enabled true

# # retrieve the registry name
registry_name=$(az acr show --name $ACR_NAME --query loginServer --output tsv)

# # retrieve the registry access key
registry_password=$(az acr credential show --name $ACR_NAME --query "passwords[0].value" --output tsv)


# Tag the Docker images
docker tag $DOCKER_IMAGE_API:$TAG $registry_name/$DOCKER_IMAGE_API:$TAG
docker tag $DOCKER_IMAGE_SCRAPER:$TAG $registry_name/$DOCKER_IMAGE_SCRAPER:$TAG
docker tag $DOCKER_IMAGE_DASHBOARD:$TAG $registry_name/$DOCKER_IMAGE_DASHBOARD:$TAG
docker tag $DOCKER_IMAGE_TRAITMENT_MCF:$TAG $registry_name/$DOCKER_IMAGE_TRAITMENT_MCF:$TAG

# Push the Docker images to the Azure Container Registry
echo $registry_password | docker login $registry_name -u $ACR_NAME --password-stdin

# docker push images
docker push $registry_name/$DOCKER_IMAGE_API:$TAG
docker push $registry_name/$DOCKER_IMAGE_SCRAPER:$TAG
docker push $registry_name/$DOCKER_IMAGE_DASHBOARD:$TAG
docker push $registry_name/$DOCKER_IMAGE_TRAITMENT_MCF:$TAG