import os
import logging
from google.cloud import storage
from pprint import pprint

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def create_storage_client():
    """Create and return a Google Cloud Storage client."""
    credentials_path = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS', '/path/to/credentials.json')
    return storage.Client.from_service_account_json(credentials_path)

def create_bucket(storage_client, bucket_name, storage_class='STANDARD', location='europe-west12'):
    """Create a new bucket in Google Cloud Storage."""
    try:
        if not storage_client.lookup_bucket(bucket_name):
            bucket = storage_client.bucket(bucket_name)
            bucket.storage_class = storage_class
            bucket.location = location
            created_bucket = storage_client.create_bucket(bucket)
            pprint(vars(created_bucket))
            return created_bucket
        else:
            logging.info(f"Bucket {bucket_name} already exists.")
    except Exception as e:
        logging.error(f"Error creating bucket: {e}")

def upload_to_bucket(storage_client, blob_name, file_path, bucket_name):
    """Upload a file to a Google Cloud Storage bucket."""
    try:
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(blob_name)
        blob.upload_from_filename(file_path)
        logging.info(f"File {file_path} uploaded to {bucket_name}/{blob_name}.")
        return True
    except Exception as e:
        logging.error(f"Error uploading file: {e}")
        return False

def download_from_bucket(storage_client, blob_name, file_path, bucket_name):
    """Download a file from a Google Cloud Storage bucket."""
    try:
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(blob_name)
        with open(file_path, 'wb') as f:
            storage_client.download_blob_to_file(blob, f)
        logging.info(f"File {blob_name} downloaded to {file_path}.")
        return True
    except Exception as e:
        logging.error(f"Error downloading file: {e}")
        return False

def main():
    bucket_name = 'python-bucket-demo'
    storage_client = create_storage_client()
    
    # Create a bucket
    create_bucket(storage_client, bucket_name)

    # Upload a file
    file_path = '/home/devboy/Downloads/waterData.zip'
    upload_to_bucket(storage_client, 'water data', file_path, bucket_name)

    # Download a file
    download_path = os.path.join(os.getcwd(), 'waterData.zip')
    download_from_bucket(storage_client, 'water data', download_path, bucket_name)

if __name__ == "__main__":
    main()
