from flask import Flask
from google.cloud import pubsub_v1, storage
import json
import os

app = Flask(__name__)

# Initialize Pub/Sub subscriber and publisher clients
subscriber = pubsub_v1.SubscriberClient()
publisher = pubsub_v1.PublisherClient()

# Initialize Google Cloud Storage client
storage_client = storage.Client()

# Set up Pub/Sub subscription and topic for publishing sorted data
subscription_path = subscriber.subscription_path('mainproject-01', 'projects/mainproject-01/subscriptions/mainCluster')
topic_path = publisher.topic_path('mainproject-01', 'sortedDataTopic')

# Name of the bucket in Google Cloud Storage
bucket_name = 'test-app-esteco'

def callback(message):
    print('Received message:', message.data)

    object_name = message.data.decode('utf-8')
    file_content = download_file_from_gcs(bucket_name, object_name)
    
    if file_content:
        sorted_data = process_and_sort_data(file_content)
        publish_sorted_data_to_topic(sorted_data)
    
    message.ack()

subscriber.subscribe(subscription_path, callback=callback)

def download_file_from_gcs(bucket_name, object_name):
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(object_name)
    
    try:
        return blob.download_as_text()
    except Exception as e:
        print(f"Error downloading file from GCS: {e}")
        return None

def process_and_sort_data(file_content):
    # Assuming the file content is JSON
    data = json.loads(file_content)
    
    # Example sorting logic (update as needed)
    sorted_data = sorted(data, key=lambda x: x['some_field'])
    
    return json.dumps(sorted_data)

def publish_sorted_data_to_topic(sorted_data):
    # Data must be a bytestring
    data = sorted_data.encode("utf-8")
    
    try:
        publish_future = publisher.publish(topic_path, data)
        publish_future.result()  # Wait for publish to complete.
        print(f"Data published to {topic_path}.")
    except Exception as e:
        print(f"Error publishing data to topic: {e}")

if __name__ == '__main__':
    app.run(debug=True)
