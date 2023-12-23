import flask
import zipfile
import io
import json
import requests

def extract_json_from_zip(zip_file):
    with zipfile.ZipFile(zip_file, 'r') as z:
        for file_name in z.namelist():
            with z.open(file_name) as f:
                yield json.load(f)

def forward_data_to_gke(json_data):
    gke_endpoint = "http://34.17.48.202/data"  # Replace with your GKE service endpoint
    response = requests.post(gke_endpoint, json=json_data)
    return response.status_code, response.text

def process_zip_file(request):
    # Ensure that we have a file in the request
    if 'file' not in request.files:
        return "No file part in the request", 400
    
    file = request.files['file']
    
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        return "No selected file", 400
    
    if file and file.filename.endswith('.zip'):
        try:
            # Process the zipped file
            for json_data in extract_json_from_zip(file):
                status_code, response_text = forward_data_to_gke(json_data)
                if status_code != 200:
                    return f"Failed to forward data to GKE: {response_text}", status_code
            
            return "File processed and data forwarded to GKE", 200

        except Exception as e:
            return f"An error occurred: {str(e)}", 500
    else:
        return "Unsupported file format", 400

# Define the Flask app and the route
app = flask.Flask(__name__)

@app.route('/process-zip', methods=['POST'])
def process_zip_route():
    return process_zip_file(flask.request)
