#!/bin/bash

logFile="/home/ubuntu/try-n-error/test-command-linux/crontab.log"
logMessage="This is a new log message."

# Add timestamp to the log message
logMessage="$(date "+%Y-%m-%d %H:%M:%S") - $logMessage"

# Write the log message to the file
echo "$logMessage" >> "$logFile"

port=3387
# Get the process ID (PID) associated with the port
pid=$(lsof -ti :$port)

if [ -z "$pid" ]; then
    echo "No process found running on port $port." >> "$logFile"
else
    # Kill the process
    echo "Killing process with PID: $pid" >> "$logFile"
    kill $pid
fi
