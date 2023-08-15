#!/bin/bash
PROXY="localhost:9050"

while IFS= read -r line; do
    hosts+=("$line")
done < <(curl -sL ransomwhat.telemetry.ltd/groups \
| jq -r '.[].locations[] | select(.available==true) | .fqdn')

hostcount=${#hosts[@]}

echo "${hostcount} hosts reportedly available"

if [ -z "${1}" ]; then
  echo -n "enter path to visit: "
  read -r path
else
  path=${1}
fi

for host in "${hosts[@]}"; do
    if [[ "${host}" == *"/" ]]; then
        host=$(echo "${host}" | sed 's/\/$//')
    fi
    if [[ "${host}" != http://* && "${host}" != https://* ]]; then
        host="http://${host}"
    fi
    response=$(curl --socks5-hostname "$PROXY" \
    -sL -w "%{http_code}" --max-time 10 "${host}${path}" -o /dev/null)
    echo "${response} ${host}${path}"
done
