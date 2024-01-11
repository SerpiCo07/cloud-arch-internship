import base64
import json
import zipfile
import io
import requests
import logging
from retrying import retry

API_GATEWAY_URL = 'https://your-api-gateway-url'  # Replace with your API Gateway URL

# Configure logging
logging.basicConfig(level=logging.INFO)

def compress_json_data(json_data):
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'a', zipfile.ZIP_DEFLATED, False) as zip_file:
        zip_file.writestr('data.json', json.dumps(json_data))
    return zip_buffer.getvalue()

@retry(stop_max_attempt_number=7, wait_exponential_multiplier=1000, wait_exponential_max=10000)
def send_to_api_gateway(zip_data):
    response = requests.post(API_GATEWAY_URL, data=zip_data, headers={'Content-Type': 'application/zip'})
    if response.status_code != 200:
        logging.error(f"Failed to send data to API Gateway: {response.text}")
        raise Exception("API request failed")
    return response.status_code, response.text

def process_pubsub_message(event, context):
    if 'data' in event:
        message_data = base64.b64decode(event['data']).decode('utf-8')
        json_data = json.loads(message_data)

        zip_data = compress_json_data(json_data)
        
        try:
            return send_to_api_gateway(zip_data)
        except Exception as e:
            logging.error(f"Failed to process message: {str(e)}")
            return "Failed to process message", 500
    else:
        logging.warning("No data in Pub/Sub message")
        return "No data in Pub/Sub message", 400