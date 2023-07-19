import os
import sys
import json
import requests
import subprocess
from dotenv import load_dotenv

def is_valid_json(json_str):
    try:
        json.loads(json_str)
    except ValueError as err:
        return False
    return True

def get_last_status_rssh_connection(unique_code_device):
    try:
        base_rest_api = os.environ.get("REST_API_RSSH_CONNECTION_STATUS")
        full_base_rest_api = base_rest_api + unique_code_device
        response = requests.get(full_base_rest_api)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")
        sys.exit(0)

def check_valid_response_last_status_rssh_connection(body_response):
    body_response_is_json = is_valid_json(body_response)
    if not body_response_is_json:
        print(f"Invalid json format")
        sys.exit(0)

    data = json.loads(body_response)
    http_code = data["http_code"]

    if 200 != http_code:
        print(f"Result http is {http_code}")
        sys.exit(0)
    return True

def send_rssh_log_to_server(unique_code_device, log, is_error):
    try:
        rest_api = os.environ.get("REST_API_RSSH_LOG")
        payload = {
            'unique_code_device': unique_code_device,
            'log': log,
            'is_error': is_error
        }
        requests.post(rest_api, payload)
    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")
        sys.exit(0)

def update_status_rssh_connection(unique_code_device, status):
    try:
        rest_api = os.environ.get("REST_API_RSSH_CONNECTION_UPDATE")
        full_rest_api = rest_api + unique_code_device
        payload = {
            'status': status
        }
        requests.put(full_rest_api, payload)
    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")

file_bat = r"C:\Users\Administrator\Documents\small-tools-reverse-ssh\python\windows-client\reverse_ssh.bat"

# Load the environment variables from .env file
load_dotenv()

status_re_run_file_bat = False
unique_code_device = os.environ.get("UNIQUE_CODE_DEVICE")

# get last connection status by unique code device
result_get_last_connection_status = get_last_status_rssh_connection(unique_code_device)
result_get_last_connection_status_string = json.dumps(result_get_last_connection_status)

# validate response
check_valid_response_last_status_rssh_connection(result_get_last_connection_status_string)

# parse body response
data_json = json.loads(result_get_last_connection_status_string)
last_rssh_connection_status = data_json["data"]["connection_status"]

if last_rssh_connection_status == os.environ.get("DISCONNECT_CONNECTION_STATUS"):
    status_re_run_file_bat = True

if last_rssh_connection_status == os.environ.get("PID_SERVER_TERMINATED_CONNECTION_STATUS"):
    status_re_run_file_bat = True

if last_rssh_connection_status == os.environ.get("PLINK_TERMINATED"):
    status_re_run_file_bat = True

if not status_re_run_file_bat:
    print(status_re_run_file_bat)
    sys.exit(0)

try:
    app_runner = os.environ.get("CMD_EXE")
    log = 'success run file bat'
    send_rssh_log_to_server(unique_code_device, log, 'no')
    update_status_rssh_connection(unique_code_device, os.environ.get("CONNECTED_CONNECTION_STATUS"))
    subprocess.call([app_runner, '/c', file_bat])
    print("done with ok")
except Exception as e:
    log = f"An error occurred: {e}"
    send_rssh_log_to_server(send_rssh_log_to_server, log, 'yes')
