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

    export GOOGLE_APPLICATION_CREDENTIALS=/path/to/your/service-account-key.json

Instead, in script we just read the environment variable.

## The Required roles of the Google Cloud Storage-bucket in order to upload/download file 
    -roles/storage.objectViewer
    -roles/storage.objectCreator
    -roles/storage.objectAdmin
    -roles/storage.admin

### storage_client_package
This package is made of two python files 
    - google_cloud_storage_manager.py 
         contains the GoogleCloudStorageManager class which encapsulates all the methods that are required to create a bucket and upload/download from it

    - main_script.py 
        - Where an instance of the oogleCloudStorageManager class is created to do one or more operations
        - The one we customize and run each time according to our needs
#### Upload the file using main_script

python3 -m storage_client_pack.main_script

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
### The especial roles that Google Cloud Function must have
 #### role/run.invoker
 While checking the permission of the GCF is in charge of being triggered by cloud storage and send a message to pubsub, you will see a Warning that says you need to run thi command : 

 gcloud functions add-invoker-policy-binding function-storage-to-pubsub \
      --region="europe-west12" \
      --member="MEMBER_NAME"

It's not correct command,since valid IAM member formats typically include:

-User: user:email@example.com
-Service Account: serviceAccount:service-account-email@example.iam.gserviceaccount.com
-Google Group: group:group-email@example.com   

Hence, the correct command you need run is as follows : 

gcloud functions add-invoker-policy-binding function-storage-to-pubsub \
    --region="europe-west12" \
    --member="serviceAccount:storage-to-pubsub@mainproject-01.iam.gserviceaccount.com"

#### role/pubsub.publisher
gcloud projects add-iam-policy-binding mainproject-01 \
    --member="serviceAccount:storage-to-pubsub@mainproject-01.iam.gserviceaccount.com" \
    --role="roles/pubsub.publisher"

NOTICE : 
 If you want to see what are the granted permissions to a service account you can use : 

 gcloud projects get-iam-policy PROJECT_ID \
    --flatten="bindings[].members" \
    --format="table(bindings.role)" \
    --filter="bindings.members:serviceAccount:SERVICE_ACCOUNT_EMAIL"

## The 2nd Google Cloud Function-DLQ watcher (GCF that listens to DLQ-sub )

 We want the second Google Cloud Function (GCF) to act as a notifier to signal Google Cloud Storage (GCS) when a message ends up in the Dead Letter Queue (DLQ) subscription. However GCS itself doesn't have a built-in mechanism to respond to such signals or notifications directly from a GCF.

 However, we can simulate a notification or signal system using GCS features like metadata updates or creating a marker file in the bucket to indicate attention is needed for a specific object.

  GCF has to have appropriate IAM permissions for accessing GCS and modifying object metadata (roles/storage.objectAdmin or a custom role with storage.objects.get and storage.objects.update permissions).

  Use the following command to deploy the python script and requirements.txt on GCF 

  gcloud functions deploy dlq_signal_function \
    --runtime python39 \
    --trigger-topic YOUR_DLQ_TOPIC_NAME \
    --set-env-vars BUCKET_NAME='your-bucket-name' \
    --entry-point dlq_signal_function \
    --source ./path/to/your/package_or_script \
    --region YOUR_FUNCTION_REGION \
    --project YOUR_PROJECT_ID


    If we wanted to use Google Cloud console to deploy this function , we must do the following :
    - import OS
    - under "Runtime, build, connections and security settings" >> "Runtime environment variables" add BUCKET_NAME


## The 3rd Google Cloud Function - re-transmitter 

  To achieve the setup where a third Google Cloud Function (GCF3) is triggered by changes in the metadata of objects within a Google Cloud Storage (GCS) bucket, and then publishes the details of those objects to a Pub/Sub topic, you will use GCS event notifications along with Cloud Functions and Pub/Sub.

  This function will filter the events to process only those where the object's metadata contains "dlq-flagged = true". Then, it publishes the object's name to the retransmitted-topic.


### Enable Pub/Sub Notifications for your GCS Bucket
 
 Set up a Pub/Sub notification for your GCS bucket to publish events to a Pub/Sub topic. This is generally done for OBJECT_FINALIZE and OBJECT_METADATA_UPDATE events. 

 '''gsutil notification create -t TOPIC_NAME -f json gs://BUCKET_NAME '''

