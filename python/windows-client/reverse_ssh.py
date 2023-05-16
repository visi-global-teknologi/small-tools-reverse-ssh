import os
from dotenv import load_dotenv
from sshtunnel import SSHTunnelForwarder

# Specify the path to the .env file
env_file = r"C:\Users\Administrator\Documents\small-tools-reverse-ssh\python\windows-client\.env"

# Load the .env file
load_dotenv(env_file)

# Reverse SSH configuration
remote_host = os.environ.get("SERVER_IP")
remote_port = os.environ.get("SERVER_PORT")
remote_username = os.environ.get("SERVER_USERNAME")
remote_password = os.environ.get("SERVER_PASSWORD")
local_host = os.environ.get("LOCAL_HOST")
local_port = os.environ.get("LOCAL_PORT")

# Create an SSH tunnel
with SSHTunnelForwarder(
    (remote_host, remote_port),
    ssh_username=remote_username,
    ssh_password=remote_password,
    remote_bind_address=(local_host, local_port)
) as tunnel:
    # Print the tunnel information
    print(f"Reverse SSH tunnel established: {tunnel.local_bind_host}:{tunnel.local_bind_port} -> {remote_host}:{remote_port}")

    # Keep the program running to maintain the SSH tunnel
    while True:
        pass
