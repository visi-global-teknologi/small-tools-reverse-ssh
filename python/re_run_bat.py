import subprocess
import requests

def post_data_to_api(url, unique_code_device, log, is_error):
    payload = {'unique_code_device': unique_code_device, 'log': log, 'is_error': is_error}
    requests.post(url, data=payload)

def call_bat(full_path_bat_file, app_runner):
    subprocess.call(['cmd.exe', '/c', batch_file])

api_url = "http://localhost:80/api/public/rssh-logs"
unique_code_device = "v7cnp"
batch_file = r"C\:Users\Administrator\Documents\wim\reverse_ssh.bat"
app_runner = 'cmd.exe'

try:
    call_bat(batch_file, app_runner)
    post_data_to_api(api_url, unique_code_device, "success re run file bat", 'no')
except subprocess.CalledProcessError as e:
    message = f"Command execution failed: {e}"
    post_data_to_api(api_url, unique_code_device, message, 'yes')
except OSError as e:
    message = f"OS error occurred: {e}"
    post_data_to_api(api_url, unique_code_device, message, 'yes')
except Exception as e:
    message = f"An error occurred: {e}"
    post_data_to_api(api_url, unique_code_device, message, 'yes')
