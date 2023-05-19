import os
import sys
import json
import psutil
import requests
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

def get_pid_app_by_name(app):
    pidNumber = None
    for proc in psutil.process_iter(['pid', 'name']):
        if app == proc.info['name']:
            pidNumber = proc.info['pid']
    return pidNumber

def kill_app_by_pid(unique_code_device, pidNumber):
    try:
        process = psutil.Process(pidNumber)
        process.terminate()
        log = f"PID {pidNumber} has been terminate"
        send_rssh_log_to_server(unique_code_device, log, 'no')
    except psutil.NoSuchProcess as e:
        # send status to server
        log = f"Error: {e}"
        send_rssh_log_to_server(unique_code_device, log, 'yes')
        sys.exit(0)

# Load the environment variables from .env file
load_dotenv()

status_terminate_plink = False
unique_code_device = os.environ.get("UNIQUE_CODE_DEVICE")
pid_server_terminated_connection_status = os.environ.get("PID_SERVER_TERMINATED_CONNECTION_STATUS")
plink_terminated_connection_status = os.environ.get("PLINK_TERMINATED_CONNECTION_STATUS")

# get last connection status by unique code device
result_get_last_connection_status = get_last_status_rssh_connection(unique_code_device)
result_get_last_connection_status_string = json.dumps(result_get_last_connection_status)

# validate response
check_valid_response_last_status_rssh_connection(result_get_last_connection_status_string)

# parse body response
data_json = json.loads(result_get_last_connection_status_string)
last_rssh_connection_status = data_json["data"]["connection_status"]

if last_rssh_connection_status == pid_server_terminated_connection_status:
    status_terminate_plink = True

if not status_terminate_plink:
    print(status_terminate_plink)
    sys.exit(0)

appName = os.environ.get("PLINK_EXE")
pidNumber = get_pid_app_by_name(appName)

if pidNumber is None:
    log = f"PID {appName} not found"
    send_rssh_log_to_server(unique_code_device, log, 'yes')
    sys.exit(0)

# kill pid & send status to server
kill_app_by_pid(pidNumber, unique_code_device)
log = f"Success kill plink.exe"
send_rssh_log_to_server(unique_code_device, log, 'no')
update_status_rssh_connection(unique_code_device, plink_terminated_connection_status)
