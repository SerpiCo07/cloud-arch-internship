import os
import logging
from storage_client_pack.google_cloud_storage_manager import GoogleCloudStorageManager

def main():
    credentials_path = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS', '/home/devboy/Downloads/mainproject-01-d30cc6b753a8.json')
    gcs_manager = GoogleCloudStorageManager(credentials_path)

    bucket_name = 'test-app-esteco'
    """
    # Create a bucket
    gcs_manager.create_bucket(bucket_name)
    """
    # Upload a file
    file_path = '/home/devboy/Downloads/estat_tec00121.tsv.gz'
    gcs_manager.upload_to_bucket('price volume ', file_path, bucket_name)
    """
    # Download a file
    download_path = os.path.join(os.getcwd(), 'waterDat.zip')
    gcs_manager.download_from_bucket('water data', download_path, bucket_name)
    """
if __name__ == "__main__":
    main()
