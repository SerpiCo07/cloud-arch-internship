import json
import os
import logging
from google.cloud import pubsub_v1
from google.api_core.exceptions import GoogleAPICallError, RetryError

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize the Pub/Sub client
publisher = pubsub_v1.PublisherClient()

# Use environment variables for the project ID and topic name
project_id = os.getenv('GCP_PROJECT_ID')
topic_name = os.getenv('GCP_TOPIC_NAME')
topic_path = publisher.topic_path(project_id, topic_name)

def notify_pubsub(event, context):
    # Construct the message
    message_json = json.dumps({
        'bucket': event['bucket'],
        'filename': event['name']
    })
    message_bytes = message_json.encode('utf-8')

    # Publish the message
    try:
        publish_future = publisher.publish(topic_path, message_bytes)
        publish_future.result()  # Verify the publish succeeded
        logging.info(f'Message published to {topic_path}')
    except (GoogleAPICallError, RetryError) as e:
        logging.error(f'Error publishing message to {topic_path}: {e}', exc_info=True)
        # Implement any retry logic or error handling here
