# ransomwatch 👀 🦅

## [ransomwatch.telemetry.ltd](https://ransomwatch.telemetry.ltd)

an onionsite scraping framework, built to watch and track ransomware blogs

> [virustotal/ransomwatch](https://www.virustotal.com/graph/embed/g75a36964bca04a668232875879a6417649d214d3dc7e4ae6a27b7465b1c15872)

groups are visited & posts are indexed within github actions - all site artefacts are dynamically generated

```shell
curl -sL ransomwhat.telemetry.ltd/posts | jq
curl -sL ransomwhat.telemetry.ltd/groups | jq
```

[![vscode](https://open.vscode.dev/badges/open-in-vscode.svg)](https://open.vscode.dev/thetanz/ransomwatch) [![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=thetanz_ransomwatch&metric=alert_status)](https://sonarcloud.io/dashboard?id=thetanz_ransomwatch) [![ransomwatch](https://github.com/thetanz/ransomwatch/actions/workflows/ransomwatch.yml/badge.svg)](https://github.com/thetanz/ransomwatch/actions/workflows/ransomwatch.yml) [![ransomwatch-build/](https://github.com/thetanz/ransomwatch/actions/workflows/ransomwatch-build.yml/badge.svg)](https://github.com/thetanz/ransomwatch/actions/workflows/ransomwatch-build.yml) [![CodeQL](https://github.com/thetanz/ransomwatch/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/thetanz/ransomwatch/actions/workflows/codeql-analysis.yml)

## technicals

 `groups.json` contains the hosts, nodes, relays and mirrors for a tracked group or actor

 `posts.json` contains parsed posts, noted by their discovery time and accountable group

### GitHub Action

[torproxy](https://github.com/thetanz/gotham) from the [**thetanz/gotham** registry](https://github.com/thetanz/gotham/pkgs/container/gotham%2Ftorproxy) exposes a tor SOCKS5 proxy to the GitHub Action through the use of a [Service Container](https://docs.github.com/en/actions/guides/about-service-containers)

the GitHub Action runs on CRON, updating this repository with findings, dynamically generating markdown reports within `docs/` which are served through GitHub Pages.

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
./ransomwhere.py add --name acmecorp --location abcdefg.onion
```

### add new mirror for an existing group

```shell
./ransomwhere.py append --name acmecorp --location abcdefghigklmnop.onion
```

## Scraping

iterates any v3 onion addressses within [groups.json](groups.json), scraping raw HTML (no headless browsers or javascript processing) into [`source/`](source)

```shell
./ransomwhere.py scrape
```

### Parsing

iterate files within the `source/` directory and contribute findings to `posts.json`

> postprocessing is done with a mix of `grep`, `awk` and `sed`. it's brittle and like any  ̴̭́H̶̤̓T̸̙̅M̶͇̾L̷͑ͅ ̴̙̏p̸̡͆a̷̛̦r̵̬̿s̴̙͛ĩ̴̺n̸̔͜g̸̘̈, has a limited lifetime.

```shell
./ransomwhere.py parse
```
