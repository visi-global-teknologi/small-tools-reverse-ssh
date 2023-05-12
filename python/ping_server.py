import requests

def post_data_to_api(url, unique_code_device):
    try:
        payload = {'unique_code_device': unique_code_device}
        response = requests.post(url, data=payload)
        response.raise_for_status()  # Check for any HTTP errors
        data = response.json()  # Get the response data in JSON format
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")

api_url = "http://localhost:80/api/public/pings"
unique_code_device = "v7cnp"
post_data_to_api(api_url, unique_code_device)
