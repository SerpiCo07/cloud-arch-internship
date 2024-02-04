from google.cloud import pubsub_v1

# Initialize the Pub/Sub publisher client with the hardcoded topic path
publisher = pubsub_v1.PublisherClient()
topic_name = 'projects/mainproject-01/topics/pubproxy'  # Full path to your topic

def publish_zip_to_topic(request):
    """
    Cloud Function to receive a zip file and publish it to a Pub/Sub topic.
    Expects a POST request with binary data of the zip file.
    """

    if request.method != 'POST':
        return 'Only POST requests are accepted', 405

    # Read the binary data of the zip file from the request
    zip_file = request.get_data()

    # Verify that data is not empty
    if not zip_file:
        return 'No data received', 400

    # Publish the zip file data to the Pub/Sub topic
    try:
        future = publisher.publish(topic_name, zip_file)
        future.result()  # Confirm the publish succeeded
        return 'Zip file published to Pub/Sub topic', 200
    except Exception as e:
        return f'An error occurred: {e}', 500
