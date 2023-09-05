##### print online hosts that do not have an enabled parser

```shell
jq -r '.[] | select(.parser == false) | select(any(.locations[]; .available == true)) | "\(.name)(\(.locations[] | select(.available == true).slug))"' groups.json
```

##### check v3 onion hosts marked as disabled are truly offline by loading each

> replace `telemetry.dark:9050` with your own proxy fqdn

```shell
jq -r '.[].locations[] | select(.enabled == false) | .slug' groups.json \
| awk 'length >= 62' | head -n 2 | xargs -I {} -P 10 \
curl --max-time 20 --socks5-hostname telemetry.dark:9050 -o /dev/null \
--silent --head --write-out '%{url_effective}: %{http_code}\n' {}
```