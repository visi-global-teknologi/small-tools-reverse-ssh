import sys
import json
import psutil
import requests

def post_data_to_api(url, unique_code_device, log, is_error):
    payload = {'unique_code_device': unique_code_device, 'log': log, 'is_error': is_error}
    requests.post(url, data=payload)

def is_valid_json(json_str):
    try:
        json.loads(json_str)
    except ValueError as err:
        return False
    return True

def get_pid_app(app):
    pidNumber = None
    for proc in psutil.process_iter(['pid', 'name']):
        if app == proc.info['name']:
            pidNumber = proc.info['pid']
    return pidNumber

def get_connection_status(url, unique_code_device):
    try:
        full_url  = url + unique_code_device
        response = requests.get(full_url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        message = f"Error occurred: {e}"
        return message

def kill_app_by_pid(pidNumber):
    try:
        process = psutil.Process(pidNumber)
        process.terminate()
        print(f"PID {pidNumber} has been terminate")
    except psutil.NoSuchProcess as e:
        # send status to server
        print(f"Error: {e}")

api_url = "http://localhost:80/api/public/rssh-connections/connection-status/"
api_url_rssh_log = "http://localhost:80/api/public/rssh-logs"
unique_code_device = "v7cnp"
appName = "plink.exe"

# get connection status
resultHitApi = get_connection_status(api_url, unique_code_device)
json_string = json.dumps(resultHitApi)
isValidJson = is_valid_json(json_string)

if not isValidJson:
    message = f"Invalid json format"
    post_data_to_api(api_url_rssh_log, unique_code_device, message, 'yes')
    sys.exit(0)

# Parse the JSON data
data = json.loads(json_string)
http_code = data["http_code"]

if 200 != http_code:
    message = f"Result http is {http_code}"
    post_data_to_api(api_url_rssh_log, unique_code_device, message, 'yes')
    sys.exit(0)

status_terminate_plink_exe = False
connection_status_rssh = data["data"]["connection_status"]

if connection_status_rssh == "disconnected":
    status_terminate_plink_exe = True

if connection_status_rssh == "request terminate":
    status_terminate_plink_exe = True

if not status_terminate_plink_exe:
    print(f"Done")
    sys.exit(0)

pidNumber = get_pid_app(appName)
if pidNumber is None:
    # send status to server
    message = f"PID {appName} not found"
    post_data_to_api(api_url_rssh_log, unique_code_device, message, 'yes')
    sys.exit()

# kill pid & send status to server
kill_app_by_pid(pidNumber)
message = f"Success kill plink.exe"
post_data_to_api(api_url_rssh_log, unique_code_device, message, 'no')
