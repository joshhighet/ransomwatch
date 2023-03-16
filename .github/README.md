<div align="center">
<h1>
  <a href="https://ransomwatch.telemetry.ltd">
    ransomwatch 👀 🦅
  </a>
</h1>
</div>

<p align="center">
  <a href="https://github.com/joshhighet/ransomwatch/actions/workflows/pylint.yml">
    <img src="https://github.com/joshhighet/ransomwatch/actions/workflows/pylint.yml/badge.svg" alt="ransomwatch pylint analysis" />
  </a>
  <a href="https://github.com/joshhighet/ransomwatch/actions/workflows/ransomwatch.yml">
    <img src="https://github.com/joshhighet/ransomwatch/actions/workflows/ransomwatch.yml/badge.svg" alt="ransomwatch engine" />
  </a>
  <a href="https://github.com/joshhighet/ransomwatch/actions/workflows/ransomwatch-build.yml">
    <img src="https://github.com/joshhighet/ransomwatch/actions/workflows/ransomwatch-build.yml/badge.svg" alt="ransomwatch dockerimage builder" />
  </a>
  <a href="https://github.com/joshhighet/ransomwatch/actions/workflows/codeql-analysis.yml">
    <img src="https://github.com/joshhighet/ransomwatch/actions/workflows/codeql-analysis.yml/badge.svg" alt="ransomwatch codeql analysis" />
  </a>
</p>

missing a group ? try the [_issue template_](https://github.com/joshhighet/ransomwatch/issues/new?assignees=&labels=✨+enhancement&template=newgroup.yml&title=new+group%3A+)

looking for historical data?  check [ransomwatch-history](https://github.com/joshhighet/ransomwatch-history)

this repository leverages github actions & pages to visit, parse & report on monitored hosts in near-realtime.

```shell
curl -sL ransomwhat.telemetry.ltd/posts | jq
curl -sL ransomwhat.telemetry.ltd/groups | jq
```

---

<h4 align="center">⚠️</h4>

<h4 align="center">
  content within ransomwatch.telemetry.ltd, posts.json, groups.json and the docs/ & source/ directories is dynamically generated based on hosting choices of real-world threat actors in near-real-time. <br><br> whilst sanitisation efforts have been taken, by viewing or accessing ransomwatch you acknowledge you are doing so at your own risk
</h4>

---

## technicals

[joshhighet/torsocc](https://github.com/joshhighet/torsocc) is introduced into the github actions workflow as a [service container](https://docs.github.com/en/actions/guides/about-service-containers) to allow onion routing within  [ransomwatch.yml](https://github.com/joshhighet/ransomwatch/blob/main/.github/workflows/ransomwatch.yml)

where possible [psf/requests](https://github.com/psf/requests) is used to fetch source html. if a javascript engine is required to render the dom [mozilla/geckodriver](https://github.com/mozilla/geckodriver) and [seleniumhq/selenium](https://github.com/SeleniumHQ/selenium) are invoked.

the frontend is ultimatley markdown, generated with [markdown.py](https://github.com/joshhighet/ransomwatch/blob/main/markdown.py) and served with [docsifyjs/docsify](https://github.com/docsifyjs/docsify) thanks to [pages.github.com](https://pages.github.com)

any graphs or visualisations are generated with [plotting.py](https://github.com/joshhighet/ransomwatch/blob/main/plotting.py) with the help of [matplotlib/matplotlib](https://github.com/matplotlib/matplotlib)

_post indexing is done with a mix of `grep`, `awk` and `sed` within [parsers.py](https://github.com/joshhighet/ransomwatch/blob/main/parsers.py) - it's brittle and like any  ̴̭́H̶̤̓T̸̙̅M̶͇̾L̷͑ͅ ̴̙̏p̸̡͆a̷̛̦r̵̬̿s̴̙͛ĩ̴̺n̸̔͜g̸̘̈, has a limited lifetime._

[`groups.json`](https://github.com/joshhighet/ransomwatch/blob/main/groups.json) contains hosts, nodes, relays and mirrors for a tracked group or actor

[`posts.json`](https://github.com/joshhighet/ransomwatch/blob/main/posts.json) contains parsed posts, noted by their discovery time and accountable group

## analysis tools

all rendered source HTML is stored within [ransomwatch/tree/main/source](https://github.com/joshhighet/ransomwatch/tree/main/source) - change tracking and revision history of these blogs is made possible with git

### [screenshotter.py](https://github.com/joshhighet/ransomwatch/blob/main/screenshotter.py)

_a script to generate high-resolution screenshots of all online hosts within `groups.json`_

### [srcanalyser.py](https://github.com/joshhighet/ransomwatch/blob/main/srcanalyser.py)

_a [beautifulsoup](https://code.launchpad.net/~leonardr/beautifulsoup/bs4) script to fetch emails, internal and external links from HTML within `source/`_

## cli operations

_fetching sites requires a local tor circuit on tcp://9050 - establish one with;_

```shell
docker run -p9050:9050 ghcr.io/joshhighet/torsocc:latest
```

### group management

_manage the groups within [groups.json](groups.json)_

#### add new location (group or additional mirror)

```shell
./ransomwatch.py add --name acmecorp --location abcdefg.onion
```

## scraping

```shell
./ransomwatch.py scrape
```

## parsing

iterate files within the `source/` directory and contribute findings to `posts.json`

> for a crude health-check across all parsers, use `assets/parsers.sh`

```shell
./ransomwatch.py parse
```

---

_ransomwatch is [licensed](https://github.com/joshhighet/ransomwatch/blob/main/LICENSE) under [unlicense.org](https://unlicense.org)_
