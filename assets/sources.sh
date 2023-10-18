#!/bin/bash

# freshonifyfe4rmuh6qwpsexfhdrww7wnt5qmkoertwxmcuvm4woo4ad.onion
# onionwsoiu53xre32jwve7euacadvhprq2jytfttb55hrbo3execodad.onion

if [ ! -d tmp ]; then
    mkdir tmp
fi

master_list=$(curl -sL ransomwhat.telemetry.ltd/groups | jq '.[].locations[].fqdn' -r)

curl -s https://telemetr.io/en/channels/1232665535-dbforall/posts \
| awk 'BEGIN{RS=" "}{if($0 ~ /http[s]?:\/\/[a-zA-Z0-9]*\.onion/){print $0}}' \
| grep -o '[a-zA-Z0-9]*\.onion' \
| grep -vE '^[a-z2-7]{16}\.onion$' \
| sort | uniq > assets/tmp/telemetr.txt

curl -s 'https://docs.google.com/spreadsheets/d/1cH4KCZJvggoHPAbk0u08Wu1vSo9ygx47QfhKD-W0TQ0/gviz/tq?tqx=out:csv' \
| cut -d ',' -f 3 \
| grep '^"http' \
| sed -e 's/^"http[s]*:\/\///' -e 's/".*//' -e 's/\/.*//' \
| grep -vE '^[a-z2-7]{16}\.onion$' \
| sort | uniq > assets/tmp/gdocs.txt

curl -s https://www.ransomlook.io/api/export/0 \
| jq -r '.[] | .locations[].fqdn' \
| sort | uniq > assets/tmp/ransomlook.txt

curl -s https://api.ransomware.live/groups \
| jq -r '.[].locations[].fqdn' \
| sort | uniq > assets/tmp/ransomwarelive.txt

curl -s https://raw.githubusercontent.com/fastfire/deepdarkCTI/main/ransomware_gang.md \
| grep -Eo 'https?://[A-Za-z0-9.-]+' \
| grep -Eo '([A-Za-z0-9.-]+\.[A-Za-z]{2,})' \
| grep -vE '^[a-z2-7]{16}\.onion$' \
| sort | uniq > assets/tmp/ddcti-ransomware_gang.txt

curl -s https://raw.githubusercontent.com/fastfire/deepdarkCTI/main/maas.md \
| grep -Eo 'http[s]?://[^)]+' \
| sed 's~^http[s]*://~~' \
| grep -vE '^[a-z2-7]{16}\.onion$' \
| sort | uniq > assets/tmp/ddcti-maas.txt

curl -s https://raw.githubusercontent.com/fastfire/deepdarkCTI/main/markets.md \
| awk -F'|' '$2 ~ /http/ {split($2, a, "/"); gsub(/\)/,"",a[3]); print a[3]}' \
| grep -vE '^[a-z2-7]{16}\.onion$' \
| sort | uniq > assets/tmp/ddcti-markets.txt

curl -s https://raw.githubusercontent.com/fastfire/deepdarkCTI/main/markets.md \
| awk -F'[()]' '{print $2}' \
| sed -n 's/^http[s]*:\/\/\([^/]*\).*$/\1/p' \
| grep -vE '^[a-z2-7]{16}\.onion$' \
| sort | uniq > assets/tmp/ddcti-markets.txt

curl -s https://raw.githubusercontent.com/fastfire/deepdarkCTI/main/forum.md \
| grep -Eo 'http[s]?://[^)]+' \
| awk -F/ '{print $3}' \
| grep -vE '^[a-z2-7]{16}\.onion$' \
| sort | uniq > assets/tmp/ddcti-forum.txt

curl -s https://www.breachsense.com/ransomware-gangs/ \
| grep '<td style=text-align:center><a' \
| cut -d '=' -f 3 \
| cut -d '>' -f 1 \
| sed 's/^"//' \
| awk -F/ '{print $3}' \
| grep -vE '^[a-z2-7]{16}\.onion$' \
| sort | uniq > assets/tmp/breachsense.txt

curl -s https://telegra.ph/Ransomware-averyware-09-15 \
| grep -oE '[^\"]*\.onion[^\"]*' \
| sed -e 's/<\/p><p> <\/p><p>/\n/g' -e 's/<\/p><p>/\n/g' -e 's/<\/p><\/article>$//g' \
| grep '\.onion' \
| grep -E '[a-z2-7]{56}\.onion' \
| sed -e 's/^ *//g' -e 's/[[:space:]]*$//' \
| grep -Eo '[^/]+\.onion' \
| grep -v 'strong>' \
| grep -v 'XSS' \
| sort | uniq > assets/tmp/telegraph-averyware.txt

curl -s https://godnotaba.ru \
| grep -oE '[a-z2-7]{56}\.onion' \
| sort | uniq > assets/tmp/godnotabaru.txt

ransomwatch_allfqdn=$(curl -sL "https://ransomwhat.telemetry.ltd/groups" | jq '.[].locations[].fqdn' -r)

is_excluded() {
    local address="$1"
    if grep -Fxq "$address" "assets/sources.exclusions"; then
        return 0 # is excluded
    else
        return 1 # not excluded
    fi
}

check_host_in_rw() {
    address="$1"
    address=$(echo "$address" | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//' -e 's/"//g')
    if is_excluded "$address"; then
        return
    fi
    if ! echo "$ransomwatch_allfqdn" | grep -q "$address"; then
        echo "$address not found in ransomwatch collection: assets/tmp/$current_file"
    fi
}

for file in assets/tmp/*; do
    if [ -f "$file" ]; then
        current_file="$(basename "$file")"
        while read -r host; do
            check_host_in_rw "$host"
        done < "$file"
    fi
done
