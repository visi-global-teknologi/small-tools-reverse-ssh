import os
import requests
import subprocess
from dotenv import load_dotenv

# Load the environment variables from .env file
load_dotenv()

def send_data_log_rssh(log, is_error):
    url = os.environ.get("URL_SERVER_RSSH_LOG")
    unique_code_device = os.environ.get("UNIQUE_CODE_DEVICE")
    payload = {
        'unique_code_device': unique_code_device,
        'log': log,
        'is_error': is_error
    }
    requests.post(url, payload)
try:
    path = os.environ.get("PATH_DIRECTORY_BATCH_FILE")
    batch_file = r"C:{}\reverse_ssh.bat".format(path)
    app_runner = os.environ.get("CMD_EXE")
    subprocess.call([app_runner, '/c', batch_file])
    log = 'success re run file bat'
    send_data_log_rssh(log, 'no')
except Exception as e:
    log = f"An error occurred: {e}"
    send_data_log_rssh(log, 'yes')
