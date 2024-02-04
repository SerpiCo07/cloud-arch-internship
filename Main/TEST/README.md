This is the documentation of a simple system to test the Google API Gateway and Google Cloud Function 

The project app-internship is the example project used in the test

# Cloud Function step by step

## Documentation
- For all the details see https://cloud.google.com/functions/docs/running/function-frameworks
- The Rest api is inspired by https://help.sonatype.com/iqserver/automating/rest-apis/user-rest-api---v2

## Installation
Install Google Cloud SDK as in guide at https://cloud.google.com/sdk/docs/install 

## Build the cloud function locally

For this test I just write a python script that opens the website of "Politecnico di Torino" and returns "Hooray!" 

## Deploy the cloud function
To deploy the function with an HTTP trigger, run the following commands :

gcloud auth login
gcloud config set project PROJECT_ID
gcloud functions deploy testFunction --region europe-west6 --entry-point check_polito --runtime python38 --trigger-http --memory 256MB --timeout 90 --max-instances 1 --service-account app-internships@appspot.gserviceaccount.com --source testFunction.zip


## Log the cloud funtion

To view logs for your function with the gcloud CLI, use the logs read command, followed by the name of the function:
```
gcloud functions logs read testFunction --region europe-west6
```

# Google API Gateeway
## Enable APIs
API Gateway requires that you enable the following Google services:
API Gateway API
Service Management API
Service Control API
and this can be done by using following commands:
```
gcloud services enable apigateway.googleapis.com
gcloud services enable servicemanagement.googleapis.com
gcloud services enable servicecontrol.googleapis.com
```
## Create APIs
Enter the following command, where:
API_ID specifies the name of your API. See API ID requirements for API naming guidelines.
PROJECT_ID specifies the name of your Google Cloud project.
```
gcloud api-gateway apis create test_api --project=api-gateway-360218
```
## Create APIs config
Before API Gateway can be used to manage traffic to your deployed API backend, it needs an API config.
``
## Create API Gateway
Now deploy the API config on a gateway. Deploying an API config on a gateway defines an external URL that API clients can use to access your API.
```

gcloud api-gateway gateways create apigateway-test --api=testapi --api-config=test-api-config --location=europe-west6 --project=app-internship
```

## Enable your API

## Create API Key
https://cloud.google.com/docs/authentication/api-keys#creating_an_api_key

api-key :
AIzaSyCa6eG7VVAxx9x84FH7YgVxJelJ69jBjwI
## Test Your API

curl -i "https://apigateway-test-cv42qqas.ew.gateway.dev/v1/user"

curl -i -X POST -H "Content-Type: application/json" "https://apigateway-test-cv42qqas.ew.gateway.dev/v1/user?key=AIzaSyCa6eG7VVAxx9x84FH7YgVxJelJ69jBjwI"

## Clean up```
gcloud api-gateway gateways delete apigateway-test --location=europe-west6 --project=app-internship

gcloud api-gateway api-configs delete test-api-config --api=testapi --project=app-internship

gcloud api-gateway apis delete testapi --project=app-internship

gcloud functions delete testFunction --region=europe-west6

also delete API Key from the Google Console 
```