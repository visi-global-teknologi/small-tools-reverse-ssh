import requests

def post_data_to_api(url, unique_code_device):
    try:
        payload = {'unique_code_device': unique_code_device}
        requests.post(url, data=payload)
    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")

api_url = "http://localhost:80/api/public/pings"
unique_code_device = "v7cnp"
post_data_to_api(api_url, unique_code_device)
