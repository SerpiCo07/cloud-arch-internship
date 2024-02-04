In this doc I explained the diffrent parts of the openAPI specification (Swagger specification version 2) and their usage

# version
On top of everything we the version of the openAPI specification is written

# x-google-backend

# x-google-management
The x-google-management extension controls different aspects of API management and contains the fields described in this section.

metrics
You use metrics in conjunction with quota and x-google-quota to configure a quota for your API. A quota lets you control the rate at which applications can call the methods in your API. 

quota
You specify the quota limit for a defined metric in the quota section.

x-google-management:
  metrics:
    - name: read-requests
      displayName: Read requests
      valueType: INT64
      metricKind: DELTA
    quota:
  limits:
    - name: read-requests-limit
      metric: read-requests
      unit: 1/min/{project}
      values:
        STANDARD: 5000

# Path
## Parameter
This is an array (or list) where you define the parameters that the endpoint expects. Parameters can be in the path (path parameters), in the query string (query parameters), headers, or in the request body

Hence,the parameter of the appZip,forwardZip and systemZip is consisted of just the characteristics of the zip file

# Responses
Something important that we need to keep in mind is that in this system requests contain at least a file (zip file) while the responses are just for the confirmation and robustness of our system

Hence the endpoints return their responses as follows : 

appZip : 
 A response status code to the application

forwardZip :
 Waits to receive "200" from the topic of the pub/sub if it did not received any status code or it receives anything but 200, it would initilize the retry logic

systemZip :
  Waits to receive "200" from the API Gateway if it did not received any status code or it receives anything but 200, it would initilize the retry logic and exponential retry logic

Therefore, the responses of the appZip,forwardZip and systemZip are just the HTTP satuts code  

However, unauthorized access (HTTP code "401") is defined globally and it's called at the operational level within each endpoint

# Update v4 to v5

## 1st update
Having had some critical issues to handle the file from appzip to forwardzip , I realized forwardzip is not really necessary and it is there since at the begining especially before the last test I did I did not know the api gateway is capable to forward the file to Pub/Sub, so I merge the two endpoints and I call it appZip

## 2nd update
Secondly, since these two endpoints appZip and systemZip send/receive from diffrent addresses,the x-google-backend extension could be defined at the operational level within each of the endpoints or each endpoint could have a diffrent configuration file where both of them are hadled by only one api gateway

>>>> Defining diffrent addresses withing a single config file

triggering the GCF with pub/sub topic instead of with HTTP trigger
create a topic/subscription for that topic

## Chanllenge : 
 apparently it's not possible to route directly from API gateway to a pub/sub !!
It seems that I need to write google cloud function to act as proxy between api gateway and the pub/sub

### Python client for Google Cloud Pub/Sub 
Google Cloud Documentation : 
https://cloud.google.com/python/docs/reference/pubsub/latest

### Creat a topic in Google Cloud Pub/Sub and Dead-Letter-Queue (DLQ)
- Set topic ID (example : testtopic)
- check the default subscription
- For encryption, choose Google managed encryption key
- while you create a topic , a default subscription will be assigned and its ID is TOPICID-SUB
- In order to create DLQ 
  - Create a topic named DLQ
  - By clicking on the testtopic-sub >> Edit
  - check Enable Dead-Letter-Queue 
  - Create a DLQ-sub and assign it to the DLQ you created before

### Creat a Google Cloud Function that routs the request from API Gateway to the Pub/Sub
Grant the pub/sub publisher role to the function 
  - create a pub/sub publisher service account 
  - While creating the google cloud function notice 
      - Allow unauthorized invocations
      - under Runtime, build, connections and security setting choose the correct service account
  - The script contains 
      - google-cloud-pub/sub library
      - The topic_name from Google Cloud Pub/Sub is copied and  mentioned in the script
        in order to tell the GCF the topic to publish the files
      - The entry point that is need while creating the GCF  is the main function
  - Deploy the script on GCF
  - The requirements.txt must include all the libraries and dependencies that are required 
    at the run time 
      - google-cloud-pubsub== [WHAT EVER IS THE VERSION ON YOUR SYSTEM] 
        google-cloud-pubsub==2.19.*
### Internal Traffic Only and Allow unauthenticated invocations

API Gateway is considered as an external service so if we set "only internall traffic" , we need a VPC connector route from api gateway to GCF !

If we set "Allow authentication" it doesn't mean each time api gateway wants to send a file to GCF they need to check the api key.

Instead of an API key, the API Gateway uses a Google-signed identity token for the authentication. This token is obtained from Google's authentication service and includes the identity of the caller (in this case, the API Gateway) - authentication with identity token

Since we want to avoid adding more services like a VPC connector and we need our API Gateway to invoke a Google Cloud Function (GCF) directly, we should choose : 
-Require Authentication
-Allow All Traffic (instead of Internal Traffic Only)

Remember: 
 even with "Allow All Traffic," it's crucial to manage access and permissions carefully. Make sure that only the necessary identities (like your API Gateway) have the IAM roles and permissions needed to invoke the Cloud Function.


### How to send request to a GCF when we "ALLOW AUTHENTICATED INVOCATIONS"

When during the creation time we choose "Allow authenticated invocations", we cannot acceess or test the GCF using a curl command easily.

We need some how show that we are authorized to access it, I tried everything from different service account with different role to api key even creating another GCF to invoke the desired function while non of them were sucessful. At the end I undrestood GCF use Oauth authentication tokens to verify the user. Hence : 

-The command below must be used in every call for GCF

```-H "Authorization: bearer $(gcloud auth print-identity-token)"```

-Let's look at it in details :
  - "Authorization: bearer $(gcloud auth print-identity-token)":
    This sets the Authorization header to use a bearer token for authentication.
    - $(gcloud auth print-identity-token): 
      This part is a shell command substitution. It runs the gcloud auth print-identity-token command, which prints an identity token for the current authenticated user in Google Cloud SDK. The result (token) is then included in the Authorization header.


-GET :
  ```curl -H "Authorization: bearer $(gcloud auth print-identity-token)" https://europe-west12-app-internships.cloudfunctions.net/function-proxy```

-POST :
  ```curl -X POST -H "Authorization: bearer $(gcloud auth print-identity-token)" https://europe-west12-app-internships.cloudfunctions.net/function-proxy ```

-POST + Path of the file :
    ```curl -X POST -H "Authorization: bearer $(gcloud auth print-identity-token)" https://europe-west12-app-internships.cloudfunctions.net/function-proxy -H "Content-Type: multipart/form-data"  -F "file=@/home/devboy/Downloads/waterDat.zip"```

# Pub/Sub gcloud command 

- Create Topic

```gcloud pubsub topics create [topic_name]```
- Create Subscription

```gcloud pubsub subscriptions create [subscription_name] --topic=[topic_name]```
- Publish a message

```gcloud pubsub topics publish topic_name --message="Your maessage"```
- Receive a message

```gcloud pubsub subscriptions pull subscription_name --auto-ack```

## Testing the api gateway + GCF + Pub/sub

api_key (it's mandatory to work with api gateway) : AIzaSyDimOlkdTKKquS9kBSUi_-L8til8snMUIU

curl -i "https://app-gateway-cv42qqas.ew.gateway.dev/v1/appZip?apikey=AIzaSyDimOlkdTKKquS9kBSUi_-L8til8snMUIU

curl -i -X POST -H "Content-Type: multipart/formdata" "https://app-gateway-cv42qqas.ew.gateway.dev" -F "file=@/home/devboy/Downloads/waterDat.zip"


# The Main Concern - How to notify the application about the failed messages

still we do not know how sholud application get notified when one or more zip files end up in DLQ 

we sholud consider different failure scenarios such as damaged file, Network errors, bad comprassion etc

# Some Ideas for updating the whole System Design
## A Storage between Application and API Gateway
 
In our last meeting, we decided on setting up a separate cloud storage for the application to upload files. This storage will trigger a REST request with the file's location or UUID through the API gateway to the cluster upon new events. The cluster will then directly retrieve the file from the storage. This approach ensures that files are transferred directly to the cluster, bypassing other services, which is a significant advantage.