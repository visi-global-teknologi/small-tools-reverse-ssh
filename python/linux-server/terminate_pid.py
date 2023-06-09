import os
import sys
import pytz
import datetime
import subprocess
from dotenv import load_dotenv
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine, Column, Integer, String, Enum, DateTime, func

# Load the environment variables from .env file
load_dotenv()

# request terminate connection status
request_terminate_connection_status = os.environ.get("REQUEST_TERMINATE_CONNECTION_STATUS")
pid_server_terminated_connection_status = os.environ.get("PID_SERVER_TERMINATED_CONNECTION_STATUS")

# Get the database connection details from environment variables
db_host = os.environ.get("DB_HOST")
db_port = os.environ.get("DB_PORT")
db_name = os.environ.get("DB_DATABASE")
db_user = os.environ.get("DB_USERNAME")
db_password = os.environ.get("DB_PASSWORD")

# Define the database connection URL
db_url = f"mysql+mysqlconnector://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

# Create the SQLAlchemy engine
engine = create_engine(db_url)

# Create a session factory
Session = sessionmaker(bind=engine)

# Create a base class for declarative models
Base = declarative_base()

# Define the device model
class ConnectionStatusModel(Base):
    __tablename__ = "connection_statuses"
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String)

# Define the rssh connection model
class RSSHConnectionModel(Base):
    __tablename__ = "rssh_connections"
    id = Column(Integer, autoincrement=True, primary_key=True)
    server_port = Column(String)
    device_id = Column(BIGINT(unsigned=True))
    connection_status_id = Column(BIGINT(unsigned=True))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

# Define the cron log model
class CronLogModel(Base):
    __tablename__ = "cron_logs"
    id = Column(Integer, autoincrement=True, primary_key=True)
    file_name = Column(String)
    log = Column(String)
    is_error = Column(Enum("no", "yes", name="is_error"))
    rssh_connection_id = Column(BIGINT(unsigned=True))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    def __init__(
        self, file_name, log, is_error, rssh_connection_id, created_at, updated_at
    ):
        self.file_name = file_name
        self.log = log
        self.is_error = is_error
        self.rssh_connection_id = rssh_connection_id
        self.created_at = created_at
        self.updated_at = updated_at

# Connect to the database
session = Session()

# get time now
def get_time_now():
    # Set the desired time zone
    timezone = pytz.timezone("Asia/Jakarta")

    # Get the current time in the specified time zone
    current_time = datetime.datetime.now(timezone)

    # Format the current time as a string
    return current_time.strftime("%Y-%m-%d %H:%M:%S")

# create data cron log
def create_cron_log(session, log, is_error, rssh_connection_id):
    new_data = CronLogModel(
        file_name="terminate_pid.py",
        log=log,
        is_error=is_error,
        rssh_connection_id=rssh_connection_id,
        created_at=get_time_now(),
        updated_at=get_time_now(),
    )
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
            log = f"Success terminated process with PID: {pid}"
            create_cron_log(session, log, "no", rssh_connection_id)
        else:
            log = f"No process found with the specified port : {port}"
            create_cron_log(session, log, "yes", rssh_connection_id)
            sys.exit(0)
    except subprocess.CalledProcessError:
        log = f"Error executing the lsof command : lsof -t -i : {port}"
        create_cron_log(session, log, "yes", rssh_connection_id)
        sys.exit(0)

def update_status_rss_connection(session, rssh_connection_id, connection_status):
    connection_status = (
        session.query(ConnectionStatusModel).filter_by(name=connection_status).first()
    )
    session.query(RSSHConnectionModel).filter(
        RSSHConnectionModel.id == rssh_connection_id
    ).update(
        {
            RSSHConnectionModel.connection_status_id: connection_status.id,
            RSSHConnectionModel.updated_at: get_time_now(),
        },
        synchronize_session=False,
    )

# Query the rss_connections table with the condition
connection_status = (
    session.query(ConnectionStatusModel)
    .filter_by(name=request_terminate_connection_status)
    .first()
)
rssh_connections = (
    session.query(RSSHConnectionModel)
    .filter_by(connection_status_id=connection_status.id)
    .all()
)

# Iterate over the retrieved connections and print the data
if rssh_connections:
    for rsshc in rssh_connections:
        id = rsshc.id
        server_port = rsshc.server_port
        terminate_process_by_port(session, server_port, id)
        update_status_rss_connection(session, id, pid_server_terminated_connection_status)
else:
    print("No request to dismiss PID")

# Close the session
session.commit()
session.close()
