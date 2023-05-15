import os
import subprocess
from sqlalchemy import create_engine, Column, Integer, String, Enum
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.dialects.mysql import BIGINT
from dotenv import load_dotenv

# Load the environment variables from .env file
load_dotenv()

# Get the database connection details from environment variables
db_host = os.environ.get('DB_HOST')
db_port = os.environ.get('DB_PORT')
db_name = os.environ.get('DB_NAME')
db_user = os.environ.get('DB_USER')
db_password = os.environ.get('DB_PASSWORD')

# Define the database connection URL
db_url = f'mysql+mysqlconnector://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'

# Create the SQLAlchemy engine
engine = create_engine(db_url)

# Create a session factory
Session = sessionmaker(bind=engine)

# Create a base class for declarative models
Base = declarative_base()

# Define the device model
class DeviceModel(Base):
    __tablename__ = "devices"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    unique_code = Column(String)
    active_status = Column(Enum("no", "yes", name="active_status"))

    def __init__(self, id, name, unique_code, active_status):
        self.id = id
        self.name = name
        self.unique_code = unique_code
        self.active_status = active_status


# Define the rssh connection model
class RSSHConnectionModel(Base):
    __tablename__ = "rssh_connections"
    id = Column(Integer, primary_key=True)
    server_port = Column(String)
    local_port = Column(String)
    device_id = Column(BIGINT(unsigned=True))
    connection_status_id = Column(BIGINT(unsigned=True))

    def __init__(self, id, server_port, local_port, device_id, connection_status_id):
        self.id = id
        self.server_port = server_port
        self.local_port = local_port
        self.device_id = device_id
        self.connection_status_id = connection_status_id

# Define the cron log model
class CronLogModel(Base):
    __tablename__ = "cron_logs"
    id = Column(Integer, primary_key=True)
    file_name = Column(String)
    log = Column(String)
    is_error = Column(Enum("no", "yes", name="is_error"))
    rssh_connection_id = Column(BIGINT(unsigned=True))

    def __init__(self, id, file_name, log, is_error, rssh_connection_id):
        self.id = id
        self.file_name = file_name
        self.log = log
        self.is_error = is_error
        self.rssh_connection_id = rssh_connection_id

# Connect to the database
session = Session()

# request terminate connection status id
request_terminate_connection_status_id = 3

# create data cron log
def create_cron_log(session, log, is_error="yes"):
    new_data = CronLogModel(file_name="terminate_pid.py", log=log, is_error=is_error)
    session.add(new_data)


# function for terminate process linux by port
def terminate_process_by_port(session, port, rssh_connection_id):
    try:
        # Execute the lsof command to get the process ID (PID) by port
        cmd = f"lsof -i :{port} -t"
        output = subprocess.check_output(cmd, shell=True).decode().strip()

        if output:
            pid = int(output)
            subprocess.call(["kill", "-9", str(pid)])
            log = f"Terminated process with PID: {pid}"
            create_cron_log(session, log, "no")
        else:
            log = f"No process found with the specified port : {port}"
            create_cron_log(session, log, "yes")
    except subprocess.CalledProcessError:
        log = f"Error executing the lsof command : lsof -t -i : {port}"
        create_cron_log(session, log, "yes")


# Query the rss_connections table with the condition
rssh_connections = (
    session.query(RSSHConnectionModel)
    .filter_by(connection_status_id=request_terminate_connection_status_id)
    .all()
)

# Iterate over the retrieved connections and print the data
if rssh_connections:
    for rsshc in rssh_connections:
        id = rsshc.id
        local_port = rsshc.local_port
        terminate_process_by_port(session, local_port, id)
else:
    log = "No request to dismiss PID"
    create_cron_log(session, log, "no")

# Close the session
session.commit()
session.close()
