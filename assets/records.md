##### print online hosts that do not have an enabled parser

```shell
curl -sL ransomwhat.telemetry.ltd/groups \
| jq -r '.[] 
  | select(
      .parser == false and 
      .captcha == false and 
      .name != "lockbit3_fs" and 
      .name != "RAMP" and
      .name != "ranion"
    ) 
  | select(
      .meta == null or 
      (.meta | contains("login page") | not) and
      (.meta | contains("decryptor") | not)
    ) 
  | select(any(.locations[]; .available == true)) 
  | "\(.name)(\(.locations[] | select(.available == true).slug))"'
```

##### check v3 onion hosts marked as disabled are truly offline by loading each

> replace `telemetry.dark:9050` with your own proxy fqdn

```shell
curl -sL ransomwhat.telemetry.ltd/groups \
| jq -r '.[].locations[] | select(.enabled == false) | .slug' \
| awk 'length >= 62' | head -n 2 | xargs -I {} -P 10 \
curl --max-time 20 --socks5-hostname telemetry.dark:9050 -o /dev/null \
--silent --head --write-out '%{url_effective}: %{http_code}\n' {}
```

##### screenshot all online hosts tagged as lockbit3

```shell
curl -sL ransomwhat.telemetry.ltd/groups \
| jq -r '.[] | select(.name == "lockbit3") | .locations[] | select(.available == true) | .slug' \
| python3 assets/screenshotter.py --stdin
```