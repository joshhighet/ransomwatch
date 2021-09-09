# ransomwatch 👀 🦅

[ransomwatch.telemetry.ltd](https://ransomwatch.telemetry.ltd)

an onionsite scraping framework, built to watch and track ransomware blogs.

30+ groups, 40+ mirrors - scraped and parsed, all within github actions

[virustotal/ransomwatch](https://www.virustotal.com/graph/embed/g75a36964bca04a668232875879a6417649d214d3dc7e4ae6a27b7465b1c15872)

```shell
curl -L ransomwhat.telemetry.ltd/posts | jq
curl -L ransomwhat.telemetry.ltd/groups | jq
```

[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=thetanz_ransomwatch&metric=alert_status)](https://sonarcloud.io/dashboard?id=thetanz_ransomwatch) [![ransomwatch](https://github.com/thetanz/ransomwatch/actions/workflows/ransomwatch.yml/badge.svg)](https://github.com/thetanz/ransomwatch/actions/workflows/ransomwatch.yml) [![ransomwatch-build/](https://github.com/thetanz/ransomwatch/actions/workflows/ransomwatch-build.yml/badge.svg)](https://github.com/thetanz/ransomwatch/actions/workflows/ransomwatch-build.yml) [![CodeQL](https://github.com/thetanz/ransomwatch/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/thetanz/ransomwatch/actions/workflows/codeql-analysis.yml)

## technicals

 `groups.json` contains the hosts, nodes, relays and mirrors for a tracked group or actor

 `posts.json` contains parsed posts, noted by their discovery time and accountable group

The core engine and SOCKS5 relay run within GitHub Actions.

As of writing a number of sites do not implement any form of CAPTCHA or alternate counter-scraping frameworks. 

By and large we just fetch the raw HTML - in some cases further effort to fetch posts is required - this is where selenium & geckodriver come into play.

### GitHub Action

[torproxy](https://github.com/thetanz/gotham) from the [**thetanz/gotham** registry](https://github.com/thetanz/gotham/pkgs/container/gotham%2Ftorproxy) exposes a tor SOCKS5 proxy to the GitHub Action through the use of a [Service Container](https://docs.github.com/en/actions/guides/about-service-containers)

The GitHub Action runs a sequence of commands with ransomwatch.py every 24 hours at 12PM NZDT, updating this repository with findings and genemrating repots within `docs/` which are served through GitHub Pages.

## Usage

_requires a local tor circuit on tcp://9050_

```shell
docker run -p9050:9050 ghcr.io/thetanz/gotham/torproxy:latest
```

## Operations

_to use the docker image, fetch it first_

```shell
docker pull ghcr.io/thetanz/ransomwatch:latest
```

## Group Management

_manage the groups within [groups.json](groups.json)_

### add new group

```shell
ransomwhere.py add --name acmecorp --location abcdefg.onion
```
_or_
```shell
docker run ghcr.io/thetanz/ransomwatch add --name acmecorp --location abcdefg.onion
```

### add new mirror for an existing group

```shell
ransomwhere.py append --name acmecorp --location abcdefghigklmnop.onion
```
_or_
```shell
docker run ghcr.io/thetanz/ransomwatch append --name acmecorp --location abcdefghigklmnop.onion
```

## Scraping

iterates any v3 onion addressses within [groups.json](groups.json), scraping raw HTML (no headless browsers or javascript processing) into [`source/`](source)

```shell
ransomwhere.py scrape
```
_or_
```shell
docker run ghcr.io/thetanz/ransomwatch scrape
```

### Parsing

iterate files within the `source/` directory and contribute findings to `posts.json`

> postprocessing is done with a mix of `grep`, `awk` and `sed`. it's brittle and like any  ̴̭́H̶̤̓T̸̙̅M̶͇̾L̷͑ͅ ̴̙̏p̸̡͆a̷̛̦r̵̬̿s̴̙͛ĩ̴̺n̸̔͜g̸̘̈, has a limited lifetime.

```shell
ransomwhere.py parse
```
_or_
```shell
docker run ghcr.io/thetanz/ransomwatch parse
```
