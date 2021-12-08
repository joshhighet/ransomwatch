<div align="center">
<h1>
  <a href="https://ransomwatch.telemetry.ltd">
    ransomwatch 👀 🦅
  </a>
</h1>
</div>

an onionsite scraping framework with the intent of tracking ransomware groups

running within github actions, groups are visited & posts are indexed within this repository at a regular cadence

_all artefacts, graphs and assets supporting [ransomwatch.telemetry.ltd](https://ransomwatch.telemetry.ltd) are dynamically generated_

[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=thetanz_ransomwatch&metric=alert_status)](https://sonarcloud.io/dashboard?id=thetanz_ransomwatch) [![ransomwatch](https://github.com/thetanz/ransomwatch/actions/workflows/ransomwatch.yml/badge.svg)](https://github.com/thetanz/ransomwatch/actions/workflows/ransomwatch.yml) [![ransomwatch-build/](https://github.com/thetanz/ransomwatch/actions/workflows/ransomwatch-build.yml/badge.svg)](https://github.com/thetanz/ransomwatch/actions/workflows/ransomwatch-build.yml) [![CodeQL](https://github.com/thetanz/ransomwatch/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/thetanz/ransomwatch/actions/workflows/codeql-analysis.yml) [![pylint](https://github.com/thetanz/ransomwatch/actions/workflows/pylint.yml/badge.svg)](https://github.com/thetanz/ransomwatch/actions/workflows/pylint.yml)

missing a group ? try the [_issue template_](https://github.com/thetanz/ransomwatch/issues/new?assignees=&labels=✨+enhancement&template=newgroup.yml&title=new+group%3A+)

```shell
curl -sL ransomwhat.telemetry.ltd/posts | jq
curl -sL ransomwhat.telemetry.ltd/groups | jq
```

#### _[virustotal/ransomwatch](https://www.virustotal.com/graph/embed/g75a36964bca04a668232875879a6417649d214d3dc7e4ae6a27b7465b1c15872)_

## technicals

[torproxy](https://github.com/thetanz/gotham) from the [**thetanz/gotham** registry](https://github.com/thetanz/gotham/pkgs/container/gotham%2Ftorproxy) is introduced into the github actions workflow as a [service container](https://docs.github.com/en/actions/guides/about-service-containers) to allow onion routing within  [ransomwatch.yml](https://github.com/thetanz/ransomwatch/blob/f939ad5d78491c7f162d8acb7b4217c1e2bd5744/.github/workflows/ransomwatch.yml)

where possible [psf/requests](https://github.com/psf/requests) is used to fetch source html. if a javascript engine is required to render the dom [mozilla/geckodriver](https://github.com/mozilla/geckodriver) and [seleniumhq/selenium](https://github.com/SeleniumHQ/selenium) are invoked.

the frontend is ultimatley markdown, generated with [markdown.py](https://github.com/thetanz/ransomwatch/blob/main/markdown.py) and served with [docsifyjs/docsify](https://github.com/docsifyjs/docsify) thanks to [pages.github.com](https://pages.github.com)

any graphs or visualisations are generated with [plotting.py](https://github.com/thetanz/ransomwatch/blob/main/plotting.py) with the help of [matplotlib/matplotlib](https://github.com/matplotlib/matplotlib)

_post indexing is done with a mix of `grep`, `awk` and `sed` within [parsers.py](https://github.com/thetanz/ransomwatch/blob/main/parsers.py) - it's brittle and like any  ̴̭́H̶̤̓T̸̙̅M̶͇̾L̷͑ͅ ̴̙̏p̸̡͆a̷̛̦r̵̬̿s̴̙͛ĩ̴̺n̸̔͜g̸̘̈, has a limited lifetime._

[`groups.json`](https://github.com/thetanz/ransomwatch/blob/main/groups.json) contains hosts, nodes, relays and mirrors for a tracked group or actor

[`posts.json`](https://github.com/thetanz/ransomwatch/blob/main/posts.json) contains parsed posts, noted by their discovery time and accountable group

## analysis tools

### [screenshotter.py](https://github.com/thetanz/ransomwatch/blob/main/screenshotter.py)

_a script to generate high-resolution screenshots of all online hosts within `groups.json`_

### [srcanalyser.py](https://github.com/thetanz/ransomwatch/blob/main/srcanalyser.py)

_a [beautifulsoup](https://code.launchpad.net/~leonardr/beautifulsoup/bs4) script to fetch emails, internal and external links from HTML within `source/`_

## cli operations

_fetching sites requires a local tor circuit on tcp://9050 - establish one with;_

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

_ransomwatch is [licensed](https://github.com/thetanz/ransomwatch/blob/main/LICENSE) under [unlicense.org](https://unlicense.org)_

---

[ransomwatch.telemetry.ltd](https://ransomwatch.telemetry.ltd)
