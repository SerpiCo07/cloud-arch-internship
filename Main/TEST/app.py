import requests
from requests.exceptions import HTTPError

def check_polito(request):
    url = 'https://www.polito.it/'
    try:
        response = requests.post(url)
        response.raise_for_status()
        return 'Hooray!', 200
    except HTTPError as http_err:
        return f'HTTP error occurred: {http_err}', 500
    except Exception as err:
        return f'Other error occurred: {err}', 500