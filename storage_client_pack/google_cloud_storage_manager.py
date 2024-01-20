import os
import logging
from google.cloud import storage

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class GoogleCloudStorageManager:
    def __init__(self, credentials_path):
        self.storage_client = storage.Client.from_service_account_json(credentials_path)

    def create_bucket(self, bucket_name, storage_class='STANDARD', location='europe-west12'):
        try:
            if not self.storage_client.lookup_bucket(bucket_name):
                bucket = self.storage_client.bucket(bucket_name)
                bucket.storage_class = storage_class
                bucket.location = location
                created_bucket = self.storage_client.create_bucket(bucket)
                logging.info(f"Bucket {created_bucket.name} created.")
                return created_bucket
            else:
                logging.info(f"Bucket {bucket_name} already exists.")
        except Exception as e:
            logging.error(f"Error creating bucket: {e}")

    def upload_to_bucket(self, blob_name, file_path, bucket_name):
        try:
            bucket = self.storage_client.get_bucket(bucket_name)
            blob = bucket.blob(blob_name)
            blob.upload_from_filename(file_path)
            logging.info(f"File {file_path} uploaded to {bucket_name}/{blob_name}.")
        except Exception as e:
            logging.error(f"Error uploading file: {e}")

    def download_from_bucket(self, blob_name, file_path, bucket_name):
        try:
            bucket = self.storage_client.get_bucket(bucket_name)
            blob = bucket.blob(blob_name)
            with open(file_path, 'wb') as f:
                self.storage_client.download_blob_to_file(blob, f)
            logging.info(f"File {blob_name} downloaded to {file_path}.")
        except Exception as e:
            logging.error(f"Error downloading file: {e}")