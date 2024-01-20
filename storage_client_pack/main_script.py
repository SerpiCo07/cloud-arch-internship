import os
import logging
from storage_client_pack.google_cloud_storage_manager import GoogleCloudStorageManager

def main():
    credentials_path = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS', '/path/to/credentials.json')
    gcs_manager = GoogleCloudStorageManager(credentials_path)

    bucket_name = 'python-bucket-demo'

    # Create a bucket
    gcs_manager.create_bucket(bucket_name)

    # Upload a file
    file_path = '/home/devboy/Downloads/waterData.zip'
    gcs_manager.upload_to_bucket('water data', file_path, bucket_name)

    # Download a file
    download_path = os.path.join(os.getcwd(), 'waterData.zip')
    gcs_manager.download_from_bucket('water data', download_path, bucket_name)

if __name__ == "__main__":
    main()
