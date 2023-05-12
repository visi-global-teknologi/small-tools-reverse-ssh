#!/bin/bash

DB_CONNECTION=mysql
DB_HOST=localhost
DB_PORT=3306
DB_DATABASE=reverse_ssh_monitoring
DB_USERNAME=root
DB_PASSWORD=
DEVICE_ID=1

# Execute a SQL query using mysql client
query="SELECT * FROM $TABLE_NAME WHERE id = $DEVICE_ID;"
result=$(mysql -h "$DB_HOST" -u "$DB_USERNAME" -p"$DB_PASSWORD" "$DB_DATABASE" -e "$query")

# Print the query result
echo "$result"
