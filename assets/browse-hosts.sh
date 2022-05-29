#!/bin/bash
# i.e `assets/browse-hosts.sh /server-status`

hosts=$(curl -sL ransomwhat.telemetry.ltd/groups \
| jq -r '.[].locations[] | select(.available==true) | .fqdn')
hostcount=$(echo ${hosts} | wc -w | tr -d ' ')

echo "${hostcount} hosts reportedly available"

if [ -z "${1}" ]; then
  echo "path to visit: " && read path
else
  path=${1}
fi

for host in ${hosts[@]}; do
    if [[ "${host}" == *"/" ]]; then
        host=$(echo "${host}" | sed 's/\/$//')
    fi
    if [[ "${host}" != *"http"* ]]; then
        host="http://${host}"
    fi
    response=$(curl --socks5-hostname localhost:9050 \
    -sL -w "%{http_code}" "${host}${path}" -o /dev/null)
    echo "${response} ${host}${path}"
done