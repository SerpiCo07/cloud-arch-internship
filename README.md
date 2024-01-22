In this Documention I will write step by step of my jeourny from creating to testing of Google cloud storage 

## Python script to Upload/Download a file from a bucket

First of all we need to make sure two APIs are enabled 
    -Google Cloud Storage
    -Google Cloud Storage JSON API

Then, we need to create a new service account with the following permissions 
    -storage object creater
    -storage object admin

Afterwards,by clicking on the sevice account we created
    -Under the "key" toolbar >> "Add Key" >> "Create new key" >> key type : JSOn
    -Download and copy its path in the sctipt that we wrote for cloud storage clinet

### Secure the service accout JSON Key
In order to avoid hardcoding the path of the Key in our code, it'd be better if set it a environmetn variable using the following command on the shell :

```export GOOGLE_APPLICATION_CREDENTIALS=/path/to/your/service-account-key.json
```
Instead, in script we just read the environment variable.

### storage_client_package
This package is made of two python files 
    - google_cloud_storage_manager.py 
         contains the GoogleCloudStorageManager class which encapsulates all the methods that are required to create a bucket and upload/download from it

    - main_script.py 
        - Where an instance of the oogleCloudStorageManager class is created to do one or more operations
        - The one we customize and run each time according to our needs

## How to notify the API Gateway a new file is uploaded in the cloud storage

The thing right now I am thinking about is having uploaded a file on our bucket , how should we notify the api gateway ?

Firstly, I'd check if GCS does have any integrated feature to help us with this matter

On the other hand,I'm thinking of creating a cloud storage triggered fucntion to hand over the files to the api gateway

### The specific roles of the Google Cloud Function to watch storage and send data directly to pub/sub
These roles are required to be granted to the service account of the google cloud function 
    - Pub/Sub Publisher
    - Service Account Token Creator
    - Eventarc Event Receiver
    - Storage Object Viewer
