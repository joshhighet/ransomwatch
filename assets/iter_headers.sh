#!/bin/bash
PROXY="telemetry.dark:9050"

online_hosts=()
while IFS= read -r host; do
    online_hosts+=("$host")
done < <(curl -sL ransomwhat.telemetry.ltd/groups \
| jq -r '.[].locations[] | select(.available==true) | .slug')

if [ ${#online_hosts[@]} -eq 0 ]; then
    echo "failed to find online hosts in dataset"
    exit 1
fi

for host in "${online_hosts[@]}"; do
    echo "fetching headers for: $host"
    curl -s -I -L --socks5-hostname "$PROXY" --max-time 10 "${host}"
    echo "---"
done
