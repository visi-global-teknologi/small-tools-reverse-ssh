import datetime
import pytz

# Set the desired time zone
timezone = pytz.timezone('Asia/Jakarta')

# Get the current time in the specified time zone
current_time = datetime.datetime.now(timezone)

# Format the current time as a string
current_time_string = current_time.strftime('%Y-%m-%d %H:%M:%S')

# Print the current time
print("Current time in Asia/Jakarta:", current_time_string)
