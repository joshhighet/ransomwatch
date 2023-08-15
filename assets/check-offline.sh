#!/bin/bash
# some hosts in groups.json are marked as inactive when they are assumed perma offline
# this script checks if they are really offline

curl -sL ransomwhat.telemetry.ltd/groups \
| jq -r '.[] | .locations[] | select(.enabled == false) | .fqdn' \
| awk 'length >= 62' \
| while read -r fqdn; do
    url="http://$fqdn"
    status=$(curl -x socks5h://telemetry.dark:9050 -o /dev/null -s -w "%{http_code}" --max-time 10 "$url" || echo "timeout")
    echo "$url: $status"
done
