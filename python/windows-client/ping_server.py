import os
import requests
from dotenv import load_dotenv

# Load the environment variables from .env file
load_dotenv()

def post_data_to_api(url, unique_code_device):
    try:
        payload = {
            'unique_code_device': unique_code_device
        }
        requests.post(url, payload)
    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")

api_url = os.environ.get("REST_API_PING")
unique_code_device = os.environ.get("UNIQUE_CODE_DEVICE")
post_data_to_api(api_url, unique_code_device)
