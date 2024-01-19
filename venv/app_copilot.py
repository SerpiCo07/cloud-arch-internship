import os
import logging
from google.cloud import storage

# Set up logging
logging.basicConfig(level=logging.INFO)

# Set environment variable
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

# Create a Cloud Storage client.
storage_client = storage.Client()

bucket_name = 'python-bucket-demo'

def upload_to_bucket(blob_name, file_path, bucket_name):
    """
    Upload file to a bucket
    :param blob_name: (str) - object name
    :param file_path: (str)
    :param bucket_name: (str)
    """
    try:
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(blob_name)
        blob.upload_from_filename(file_path)
        return True
    except storage.exceptions.GoogleCloudError as e:
        logging.error(e)
        return False

def download_from_bucket(blob_name, file_path, bucket_name):
    """
    Download file from a bucket
    :param blob_name: (str) - object name
    :param file_path: (str)
    :param bucket_name: (str)
    """
    try:
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(blob_name)
        with open(file_path, 'wb') as f:
            storage_client.download_blob_to_file(blob, f)
        return True
    except storage.exceptions.GoogleCloudError as e:
        logging.error(e)
        return False

# Use the functions
file_path = '/home/devboy/Downloads/waterData.zip'
upload_to_bucket('water data', os.path.join(file_path, 'waterData.zip'), bucket_name)
download_from_bucket('water data', os.path.join(os.getcwd(), 'waterData.zip'), bucket_name)