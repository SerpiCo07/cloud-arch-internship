from google.cloud import storage
import base64
import json
import logging
from typing import Dict

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class GCSObjectManager:
    def __init__(self, bucket_name: str):
        self.bucket_name = bucket_name
        self.storage_client = storage.Client()
        self.bucket = self.storage_client.bucket(bucket_name)

    def object_exists(self, object_name: str) -> bool:
        blob = self.bucket.blob(object_name)
        return blob.exists()

    def update_object_metadata(self, object_name: str, metadata: Dict[str, str]) -> bool:
        if not self.object_exists(object_name):
            logging.error(f"Object {object_name} does not exist in bucket {self.bucket_name}.")
            return False
        
        try:
            blob = self.bucket.blob(object_name)
            blob.metadata = metadata
            blob.patch()
            logging.info(f"Updated metadata for {object_name} in {self.bucket_name}.")
            return True
        except Exception as e:
            logging.error(f"Failed to update metadata for {object_name} in {self.bucket_name}. Error: {e}")
            return False

def dlq_signal_function(event: Dict, context: 'google.cloud.functions.Context'):
    """
    Triggered by messages on the DLQ subscription. Extracts the object name and signals GCS.
    """
    if 'data' in event:
        message_content = base64.b64decode(event['data']).decode('utf-8')
        message_json = json.loads(message_content)

        # Extract bucket name and object name
        bucket_name = message_json.get('bucket')
        object_name = message_json.get('filename')

        if bucket_name and object_name:
            # Create an instance of GCSObjectManager and update object metadata as a signal
            gcs_manager = GCSObjectManager(bucket_name)
            metadata = {"dlq-flagged": "true"}
            gcs_manager.update_object_metadata(object_name, metadata)
        else:
            logging.warning("Bucket name or object name not found in the DLQ message.")
    else:
        logging.warning("No data found in the DLQ message.")