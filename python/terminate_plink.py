import os
import sys
import json
import psutil
import requests
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

def get_pid_app_by_name(app):
    pidNumber = None
    for proc in psutil.process_iter(['pid', 'name']):
        if app == proc.info['name']:
            pidNumber = proc.info['pid']
    return pidNumber

def kill_app_by_pid(pidNumber, unique_code_device):
    try:
        process = psutil.Process(pidNumber)
        process.terminate()
        message = f"PID {pidNumber} has been terminate"
        post_data_log_to_server(unique_code_device, message, 'no')
    except psutil.NoSuchProcess as e:
        # send status to server
        message = f"Error: {e}"
        post_data_log_to_server(unique_code_device, message, 'yes')

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

status_terminate_plink_exe = False
connection_status_rssh = data["data"]["connection_status"]

if connection_status_rssh == "disconnected":
    status_terminate_plink_exe = True

if connection_status_rssh == "request terminate":
    status_terminate_plink_exe = True

if not status_terminate_plink_exe:
    message = "no connection status required for restart"
    post_data_log_to_server(unique_code_device, message, 'no')
    sys.exit(0)

appName = os.environ.get("PLINK_EXE")
pidNumber = get_pid_app_by_name(appName)

if pidNumber is None:
    message = f"PID {appName} not found"
    post_data_log_to_server(unique_code_device, message, 'yes')
    sys.exit(0)

# kill pid & send status to server
kill_app_by_pid(pidNumber, unique_code_device)
message = f"Success kill plink.exe"
post_data_log_to_server(unique_code_device, message, 'no')
