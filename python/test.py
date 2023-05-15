import os
from dotenv import load_dotenv

# Load the environment variables from .env file
load_dotenv()

# request terminate connection status
request_terminate_connection_status = os.environ.get('REQUEST_TERMINATE_CONNECTION_STATUS')
print(request_terminate_connection_status)
