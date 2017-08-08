#!/bin/bash

source $1


  
if [ -z "$war" ]; then
  printf '{"failed": true, "msg": "missing required arguments: war"}'
  exit 1
fi

if [ -z "$url" ]; then
  printf '{"failed": true, "msg": "missing required arguments: url"}'
  exit 1
fi

if [ -z "$username" ]; then
  printf '{"failed": true, "msg": "missing required arguments: username"}'
  exit 1
fi

if [ -z "$password" ]; then
  printf '{"failed": true, "msg": "missing required arguments: password"}'
  exit 1
fi

result=$(curl -s --upload-file $war "http://$username:$password@$url/manager/text/deploy?path=/mnt-exam&update=true")

time=$(date)

if [[ $result == *"OK"* ]]; then
	printf '{"failed": false, "changed": true,  "msg": "Successful deployment", "time": "%s", "user": "%s"}' "$time" "$username"
	exit 0
fi

echo $result
printf '{"failed": true, "msg": "Failed to deploy app"}'

exit 0
