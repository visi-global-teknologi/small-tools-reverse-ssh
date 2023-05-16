import os
import paramiko
from dotenv import load_dotenv

# Specify the path to the .env file
env_path = '/.env'

# Load the .env file
load_dotenv(env_path)

# Reverse SSH configuration
remote_host = os.environ.get("SERVER_IP")
remote_port = os.environ.get("SERVER_PORT")
remote_username = os.environ.get("SERVER_USERNAME")
remote_password = os.environ.get("SERVER_PASSWORD")
local_host = os.environ.get("LOCAL_HOST")
local_port = os.environ.get("LOCAL_PORT")

# Create an SSH client
ssh_client = paramiko.SSHClient()
ssh_client.load_system_host_keys()

# Establish SSH connection to the remote host
ssh_client.connect(remote_host, remote_port, remote_username, remote_password)

# Set up a reverse SSH tunnel
reverse_tunnel = ssh_client.reverse_port_forward(local_port, local_host, remote_port)

# Print the tunnel information
print(f"Reverse SSH tunnel established: {local_host}:{reverse_tunnel[1]} -> {remote_host}:{remote_port}")

# Keep the program running to maintain the SSH tunnel
while True:
    pass

# Close the SSH connection
ssh_client.close()
