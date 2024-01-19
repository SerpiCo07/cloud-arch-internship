import os
from google.cloud import storage
from pprint import pprint 

#set environment variable
os.environ['GOOGLE_APPLICATION_CREDENTIALS']='/home/devboy/Downloads/mainproject-01-d30cc6b753a8.json'

# Create a Cloud Storage client.
storage_client=storage.Client()

#print(dir(storage_client))

bucket_name='python-bucket-demo'

"""
Create a bucket
"""
"""

bucket=storage_client.bucket(bucket_name)
bucket.storage_class='STANDARD'
bucket.location='europe-west12'
bucket=storage_client.create_bucket(bucket)

pprint(vars(bucket))

"""

"""
Get a bucket
"""
my_bucket=storage_client.get_bucket('test-app-esteco')
pprint(vars(my_bucket))

"""
Upload a file
"""

def Upload_to_bucket(blob_name,file_path, bucket_name):
    '''
    Upload file to a bucket
    : blob_name  (str) - object name
    : file_path (str)
    : bucket_name (str)
    '''
    try:
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(blob_name)
        blob.upload_from_filename(file_path)
        return True
    except Exception as e:
        print(e)
        return False
    
file_path=r'/home/devboy/Downloads/waterData.zip'

Upload_to_bucket('water data',os.path.join(file_path,'waterData.zip'),bucket_name)

"""
Download a file
"""

def Download_from_bucket(blob_name,file_path, bucket_name):
    try:
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(blob_name)
        with open(file_path,'wb') as f:
            storage_client.download_blob_to_file(blob,f)
        return True
    except Exception as e:
        print(e)
        return False

Download_from_bucket('water data',os.path.join(os.getcwd(),'waterData.zip'),bucket_name)