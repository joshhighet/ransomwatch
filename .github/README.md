# ransomwatch 👀 🦅

## [ransomwatch.telemetry.ltd](https://ransomwatch.telemetry.ltd)
#### _[virustotal/ransomwatch](https://www.virustotal.com/graph/embed/g75a36964bca04a668232875879a6417649d214d3dc7e4ae6a27b7465b1c15872)_

ransomwatch is an onionsite scraping framework, built to watch and track ransomware blogs

groups are visited & posts are indexed every half hour within this repository - all artefacts, graphs and  assets are dynamically generated

[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=thetanz_ransomwatch&metric=alert_status)](https://sonarcloud.io/dashboard?id=thetanz_ransomwatch) [![ransomwatch](https://github.com/thetanz/ransomwatch/actions/workflows/ransomwatch.yml/badge.svg)](https://github.com/thetanz/ransomwatch/actions/workflows/ransomwatch.yml) [![ransomwatch-build/](https://github.com/thetanz/ransomwatch/actions/workflows/ransomwatch-build.yml/badge.svg)](https://github.com/thetanz/ransomwatch/actions/workflows/ransomwatch-build.yml) [![CodeQL](https://github.com/thetanz/ransomwatch/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/thetanz/ransomwatch/actions/workflows/codeql-analysis.yml) [![pylint](https://github.com/thetanz/ransomwatch/actions/workflows/pylint.yml/badge.svg)](https://github.com/thetanz/ransomwatch/actions/workflows/pylint.yml)

## technicals

_missing a group you know about? [use this issue template](https://github.com/thetanz/ransomwatch/issues/new?assignees=&labels=✨+enhancement&template=newgroup.yml&title=new+group%3A+)_

`groups.json` contains the hosts, nodes, relays and mirrors for a tracked group or actor

`posts.json` contains parsed posts, noted by their discovery time and accountable group

```shell
curl -sL ransomwhat.telemetry.ltd/posts | jq
curl -sL ransomwhat.telemetry.ltd/groups | jq
```

[torproxy](https://github.com/thetanz/gotham) from the [**thetanz/gotham** registry](https://github.com/thetanz/gotham/pkgs/container/gotham%2Ftorproxy) is introduced into the workflow as a [service container](https://docs.github.com/en/actions/guides/about-service-containers) to allow onion routing within  [ransomwatch.yml](https://github.com/thetanz/ransomwatch/blob/f939ad5d78491c7f162d8acb7b4217c1e2bd5744/.github/workflows/ransomwatch.yml) on CRON

where possible [psf/requests](https://github.com/psf/requests) is used to fetch source html. if a javascript engine is required to render the dom [mozilla/geckodriver](https://github.com/mozilla/geckodriver) and [seleniumhq/selenium](https://github.com/SeleniumHQ/selenium) are invoked.

the frontend is ultimatley markdown, generated with [markdown.py](https://github.com/thetanz/ransomwatch/blob/main/markdown.py) and served with [docsifyjs/docsify](https://github.com/docsifyjs/docsify) thanks to [pages.github.com](https://pages.github.com)

any graphs or visualisations are generated within the workflow with the help of [plotly/plotly.py](https://github.com/plotly/plotly.py)

_post indexing is done with a mix of `grep`, `awk` and `sed`. it's brittle and like any  ̴̭́H̶̤̓T̸̙̅M̶͇̾L̷͑ͅ ̴̙̏p̸̡͆a̷̛̦r̵̬̿s̴̙͛ĩ̴̺n̸̔͜g̸̘̈, has a limited lifetime._

## cli operations

_fetching sites requires a local tor circuit on tcp://9050_

```shell
docker run -p9050:9050 ghcr.io/thetanz/gotham/torproxy:latest
```

### group management

_manage the groups within [groups.json](groups.json)_

#### add new group

```shell
./ransomwhere.py add --name acmecorp --location abcdefg.onion
```

#### add new mirror for an existing group

```shell
./ransomwhere.py append --name acmecorp --location abcdefghigklmnop.onion
```

## scraping

```shell
./ransomwhere.py scrape
```

## parsing

iterate files within the `source/` directory and contribute findings to `posts.json`

```shell
./ransomwhere.py parse
```

---

[ransomwatch.telemetry.ltd](https://ransomwatch.telemetry.ltd)