from flask import Flask
from google.cloud import pubsub_v1
import json
import requests

app=Flask(__name__)
subscriber=pubsub_v1.SubscriberClient()


#set up pub\sub subscription

subscription_path=subscriber.subscription_path('mainproject-01','projects/mainproject-01/subscriptions/mainCluster')

def callback(message):
    print('Received message',message.data)
    #process the message
    sorted_data=process_data(message.data)
    #send the sorted data to the cloud function
    send_to_cloud_function(sorted_data)
    message.ack()

subscriber.subscribe(subscription_path,callback=callback)

#define data processing function

def process_data(data):
    
    #Convert data from bytes to a JSON object
    json_data=json.loads(data.decode('utf-8'))

    #perform sorting or the othr processing
    sorted_data = sort_json_data(json_data)
    return sorted_data

#define function to send data to Googel Cloud Function

def send_to_cloud_function(data):
    url="..."
    headers={'Content-Type': 'application/json'}
    response = requests.post(url,headers=headers,json=data)
    print("Data sent to CLoud Function, response :",response.text)

    

