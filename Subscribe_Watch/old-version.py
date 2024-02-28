from google.cloud import storage
import base64
import json

def update_object_metadata(bucket_name, object_name):
    """
    Updates metadata for the specified object to signal that it has been flagged by the DLQ process.
    """
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(object_name)
    
    if not blob.exists():
        print(f"Object {object_name} does not exist in bucket {bucket_name}.")
        return
    
    # Update metadata to signal attention needed
    metadata = {"dlq-flagged": "true"}
    blob.metadata = metadata
    blob.patch()
    print(f"Updated metadata for {object_name} in {bucket_name} to signal DLQ processing.")

def dlq_signal_function(event, context):
    """
    Triggered by messages on the DLQ subscription. Extracts the object name and signals GCS.
    """
    if 'data' in event:
        message_content = base64.b64decode(event['data']).decode('utf-8')
        message_json = json.loads(message_content)
        
        # Extract bucket name and object name
        bucket_name = message_json.get('bucket')
        object_name = message_json.get('filename')
        
        # Update object metadata as a signal
        update_object_metadata(bucket_name, object_name)
    else:
        print("No data found in the DLQ message.")
