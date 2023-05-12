import requests
import pprint

def post_data_to_api(url, unique_code):
    try:
        payload = {'unique_code': unique_code}
        response = requests.post(url, data=payload)
        response.raise_for_status()  # Check for any HTTP errors
        data = response.json()  # Get the response data in JSON format
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")

# Example usage:
api_url = "http://localhost:80/api/public/ping"
unique_code = "v7cnp"
api_data = post_data_to_api(api_url, unique_code)
if api_data:
    formatted_data = pprint.pformat(api_data)
    print(formatted_data)
