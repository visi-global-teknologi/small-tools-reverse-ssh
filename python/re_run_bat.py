import os
import sys
import json
import requests
import subprocess
from dotenv import load_dotenv

# Load the environment variables from .env file
load_dotenv()

def is_valid_json(json_str):
    try:
        json.loads(json_str)
    except ValueError as err:
        return False
    return True

def post_data_log_to_server(unique_code_device, log, is_error):
    api_url = os.environ.get("URL_SERVER_RSSH_LOG")
    payload = {
        'unique_code_device': unique_code_device,
        'log': log,
        'is_error': is_error
    }
    requests.post(api_url, payload)

def get_last_status_rssh_connection(unique_code_device):
    try:
        api_url = os.environ.get("URL_SERVER_CONNECTION_STATUS")
        full_api_url = api_url + unique_code_device
        response = requests.get(full_api_url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return f"Error occurred: {e}"

def send_data_log_rssh(unique_code_device, log, is_error):
    url = os.environ.get("URL_SERVER_RSSH_LOG")
    payload = {
        'unique_code_device': unique_code_device,
        'log': log,
        'is_error': is_error
    }
    requests.post(url, payload)

unique_code_device = os.environ.get("UNIQUE_CODE_DEVICE")
# get last connection status
result_get_last_connection_status = get_last_status_rssh_connection(unique_code_device)
json_string = json.dumps(result_get_last_connection_status)

# check response data is json
isValidJson = is_valid_json(json_string)

if not isValidJson:
    message = f"Invalid json format"
    post_data_log_to_server(unique_code_device, message, 'yes')
    sys.exit(0)

# Parse the JSON data
data = json.loads(json_string)
http_code = data["http_code"]

if 200 != http_code:
    message = f"Result http is {http_code}"
    post_data_log_to_server(unique_code_device, message, 'yes')
    sys.exit(0)

status_re_run_file_bat = False
connection_status_rssh = data["data"]["connection_status"]

if connection_status_rssh == "disconnected":
    status_re_run_file_bat = True

if connection_status_rssh == "terminated":
    status_re_run_file_bat = True

if not connection_status_rssh:
    message = "no connection status required for re-run file bat"
    post_data_log_to_server(unique_code_device, message, 'no')
    sys.exit(0)

try:
    path = os.environ.get("PATH_DIRECTORY_BATCH_FILE")
    batch_file = r"C:{}\reverse_ssh.bat".format(path)
    app_runner = os.environ.get("CMD_EXE")
    subprocess.call([app_runner, '/c', batch_file])
    log = 'success re run file bat'
    send_data_log_rssh(unique_code_device, log, 'no')
except Exception as e:
    log = f"An error occurred: {e}"
    send_data_log_rssh(unique_code_device, log, 'yes')
