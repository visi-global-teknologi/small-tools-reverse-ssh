import sys
import psutil

def get_pid_app(app):
    pidNumber = None
    for proc in psutil.process_iter(['pid', 'name']):
        if app == proc.info['name']:
            pidNumber = proc.info['pid']

    return pidNumber

def kill_app_by_pid(pidNumber):
    try:
        process = psutil.Process(pidNumber)
        process.terminate()
        print(f"PID {pidNumber} has been terminate")
    except psutil.NoSuchProcess as e:
        # send status to server
        print(f"Error: {e}")

appName = "plink.exe"
pidNumber = get_pid_app(appName)

if pidNumber is None:
    # send status to server
    print(f"PID {appName} not found")
    sys.exit()

# kill pid & send status to server
kill_app_by_pid(pidNumber)
