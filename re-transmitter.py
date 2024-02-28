from google.cloud import pubsub_v1
import base64
import json
import os

publisher = pubsub_v1.PublisherClient()
destination_topic_path = publisher.topic_path(os.getenv('GCP_PROJECT_ID'), 'DESTINATION_TOPIC_NAME')

def publish_object_details(event, context):
    """Publishes the object's details to another Pub/Sub topic upon metadata change."""
    data = base64.b64decode(event['data']).decode('utf-8')
    event_data = json.loads(data)
    
    # Check for metadata update events
    if 'metadata' in event_data:
        object_info = {
            'bucket': event_data['bucket'],
            'name': event_data['name'],
            'metadata': event_data['metadata']
        }
        
        # Publish object information to the destination topic
        message_str = json.dumps(object_info)
        message_bytes = message_str.encode('utf-8')
        publish_future = publisher.publish(destination_topic_path, message_bytes)
        publish_future.result()
        
        print(f"Published object details to {destination_topic_path}")

# Note: Ensure to replace 'DESTINATION_TOPIC_NAME' with your actual destination topic name.
