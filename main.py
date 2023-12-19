import zipfile
import io
import json
from google.cloud import pubsub_v1

# Initialize the Pub/Sub client
publisher = pubsub_v1.PublisherClient()
topic_name = 'projects/mainproject-01/topics/mainFunc'  # Replace with your GCP project ID and Pub/Sub topic ID

def extract_json_from_zip(zip_file):
    with zipfile.ZipFile(zip_file, 'r') as z:
        for file_name in z.namelist():
            with z.open(file_name) as f:
                yield json.load(f)

def forward_data_to_pubsub(json_data):
    data_str = json.dumps(json_data)  # Convert JSON data to a string
    data_bytes = data_str.encode("utf-8")  # Convert string to bytes
    future = publisher.publish(topic_name, data_bytes)  # Publish to Pub/Sub
    return future.result()  # Wait for publish to complete

def process_zip_file(request):
    if not request.data:
        return "No data in the request", 400

    try:
        zip_file = io.BytesIO(request.data)
        for json_data in extract_json_from_zip(zip_file):
            forward_data_to_pubsub(json_data)
        return "File processed and data forwarded to Pub/Sub", 200
    except zipfile.BadZipFile:
        return "Invalid or corrupt zip file", 400
    except Exception as e:
        return f"An error occurred: {str(e)}", 500
