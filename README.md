In this documentation, I have provided a step-by-step guide on how to create a simple web application using Flask and how to set up a cluster using Google Kubernetes Engine (GKE), followed by instructions on deploying the application onto GKE.

## Web-app using FLASK 
This flask app is supposed to the following tasks :
    
- Receive the name of an object from a pub/sub subscriber
- Ask the bucket within the Google Cloud Storage to send the file directly having giving its name withing the bucket 
- Sort all data within the file
- Send its output to a topic on pub/sub
 
 
 Here's a high-level overview of steps we follow, along with adjustments to ensure smooth interaction between GCS and your Flask application running in GKE:
- Containerize Your Flask Application
- Build and Push the Docker Image
- Prepare GKE for Deployment
- Deploy to GKE >> deployment.yaml
- Expose Your Application >> service.yaml

Moreover, don't forget to adjust GCS and GKE for interaction :
- Authentication :
        Since our application interacts with GCS, we should ensure our GKE pods have the correct permissions. With Workload Identity, we can bind Kubernetes service accounts to Google Cloud service accounts with the necessary GCS permissions.
- Configuration :
        Manage sensitive configurations and credentials using Kubernetes Secrets or ConfigMaps, and reference these in your deployment configuration.

## Containerize Your Flask Application

Enable the following APIs:
-Artifact Registry
-Cloud Build
-Google Kubernetes Engine APIs


## Containerizing an app with Cloud Build

```The general approach we store our container on Artifact Registry then we deploy it on Cluster from that registry ```

Enable the following APIs:
-Artifact Registry
-Cloud Build
-Google Kubernetes Engine APIs

1-create app.py file
2-create Dockerfile
3-Create .dockerignore file
4-create Artifact Registry using the following gcloud command

gcloud artifacts repositories create test-repo \
    --project=PROJECT_ID \
    --repository-format=docker \
    --location= europe-west12 \
    --description="Docker repository"

5- Build your container image using Cloud Build :

It's similar to run ```docker build ``` and ```docker push ``` but the build happens on cloud



[HOSTNAME]/[PROJECT-ID]/[REPOSITORY]/[IMAGE]:[TAG]

```gcloud builds submit Main/ --tag europe-west12-docker.pkg.dev/app-internships/test-repo/flask-app:first```

Note : "TEST" in the command above shows the sub-directory where Dockerfile is stored

### Image/(s) on Artifact Repository 

```gcloud artifacts docker images list [REPOSITORY_NAME] --project=[PROJECT_ID]```

-Example:
 gcloud artifacts docker images list europe-west12-docker.pkg.dev/mainproject-01/test-repo --project=mainproject-01

## Creating a GKE cluster

A GKE cluster is a managed set of Compute Engine virtual machines that operate as a single GKE cluster.

There are two different approaches to create a cluster on GKE. Using "create-auto" - an autopilot cluster- GCP itself handles all the underlying operations such as managing the nodes and pods, networking etc. On the other hand, "Create" is the standard way of creating a cluster and handling all the operations are on the developers.

In this test, we use "create-auto" 

1- Create a cluster

```gcloud container clusters create-auto test-gke --location europe-west12```

Having run the gcloud command above you may encounter an error according to "gke-gcloud-auth-plugin"
- First of all, check for updates
  
  ```gcloud components update ```

- Secondly, you may need to install the auth-plugin using: 
  
  ```gcloud components install gke-gcloud-auth-plugin```


## Deploying to GKE

To deploy your app to the GKE cluster you created, you need two Kubernetes objects.

- A "Deployment" to define your app.
- A "Service" to define how to access your app

### Authentication - JSON key from the service account 

#### Create Kubernetes secret form JSON key

```kubectl create secret generic my-service-account --from-file=key.json=/path/to/your/service-account-file.json ```

kubectl create secret generic my-service-account --from-file=key.json=C:\Cluster-repo\Main\app-internships-902d82f09872.json

NOTE : 
        Then, modify your Deployment manifest to mount the secret as a volume or set it as an environment variable

### demployment.yaml

1-Create deployment.yaml file 
2-Deploy deployment.yaml file to cluster
 
  ```kubectl apply -f deployment.yaml```

3-Track the status of deployment

```kubectl get deployments```
The Deployment is complete when all of the "AVAILABLE" deployments are "READY".

Note : If the Deployment has a mistake, run kubectl apply -f deployment.yaml again to update the Deployment with any changes.

4- After the Deployment is complete, you can see the Pods that the Deployment created:

```kubectl get pods```

### Service.yaml

1- Create the service.yaml file
2- Create the test-app Service:

  ```kubectl apply -f service.yaml```

3- Get the "external IP-address" for the service : 

  ```kubectl get services```

Note : If the application requires complex routing or SSL/TLS we need to add "Ingress"

## View a deployed app

 ```http://[EXTERNAL-IP]:80```

 ```curl [EXTERNAL_IP]:80```

 Also we can check the application logs 

 ```kubectl logs [pod's name]```

## Clean up

1- Delete a cluster using the Google Cloud CLI

```gcloud container clusters delete test-gke --location europe-west12 --quiet```

2-  Delete an image in your Artifact Registry repository

```gcloud artifacts docker images delete europe-west12-docker.pkg.dev/mainproject-01/test-repo/test-app:first --quiet```