# An bried explanation on different parts of openAPI specification
# version
On top of everything we the version of the openAPI specification is written

# x-google-backend
To address the URL that api gateway needs to interact with

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
 
