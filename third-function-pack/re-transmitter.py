import base64
import json
import logging
import os
from google.cloud import pubsub_v1, storage
from google.auth import default
from typing import Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Dynamically obtain the current project ID
_, project_id = default()

# Initialize the Pub/Sub client
publisher = pubsub_v1.PublisherClient()

# Retrieve environment variable for the topic name
topic_name = os.getenv('TOPIC_NAME')
if not topic_name:
    logging.error("Environment variable 'TOPIC_NAME' not set.")
    raise EnvironmentError("Environment variable 'TOPIC_NAME' not set.")

# Construct the full Pub/Sub topic path
topic_path = publisher.topic_path(project_id, topic_name)

def publish_to_topic(object_info: Dict[str, Any]):
    """Publishes object information to the specified Pub/Sub topic."""
    try:
        message_str = json.dumps(object_info)
        message_bytes = message_str.encode("utf-8")
        publish_future = publisher.publish(topic_path, message_bytes)
        publish_future.result()  # Wait for the publish to complete
        logging.info(f"Published object info to {topic_path}: {object_info}")
    except Exception as e:
        logging.error(f"Failed to publish to {topic_path}: {e}", exc_info=True)

def metadata_change_trigger(event: Dict, context):
    """Triggered by GCS events. Filters for metadata changes indicating dlq-flagged objects."""
    # Retrieve environment variable for the bucket name
    bucket_name = os.getenv('BUCKET_NAME')
    if not bucket_name:
        logging.error("BUCKET_NAME environment variable not set.")
        return

    # Decode the event data and process
    data = base64.b64decode(event['data']).decode('utf-8')
    message = json.loads(data)

    # Extract object name from the event data
    object_name = message.get('name')
    if not object_name:
        logging.warning("Object name not found in the event data.")
        return

    # Create a client to interact with GCS
    storage_client = storage.Client()
    # Get the GCS bucket
    bucket = storage_client.bucket(bucket_name)
    # Get the blob from the bucket
    blob = bucket.blob(object_name)

    # Check if the object's metadata indicates it should be retransmitted
    if blob.exists() and blob.metadata and blob.metadata.get('dlq-flagged') == 'true':
        # Create the object information to publish
        object_info = {'bucket': bucket_name, 'filename': object_name}
        # Publish the object information to the specified Pub/Sub topic
        publish_to_topic(object_info)
    else:
        logging.info(f"No retransmission flag found for {object_name} in {bucket_name}")
