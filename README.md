![](https://avatars0.githubusercontent.com/u/2897191?s=90&v=4)

# ransomwatch 👀 🦅

[ransomwatch.telemetry.ltd/report](https://ransomwatch.telemetry.ltd/report)

an onionsite scraping framework, built to watch and track ransomware blogs.

[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=thetanz_ransomwatch&metric=alert_status)](https://sonarcloud.io/dashboard?id=thetanz_ransomwatch) [![ransomwatch](https://github.com/thetanz/ransomwatch/actions/workflows/ransomwatch.yml/badge.svg)](https://github.com/thetanz/ransomwatch/actions/workflows/ransomwatch.yml) [![ransomwatch-build/](https://github.com/thetanz/ransomwatch/actions/workflows/ransomwatch-build.yml/badge.svg)](https://github.com/thetanz/ransomwatch/actions/workflows/ransomwatch-build.yml) [![CodeQL](https://github.com/thetanz/ransomwatch/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/thetanz/ransomwatch/actions/workflows/codeql-analysis.yml)

## technicals

 `groups.json` dictionary handles multiple nodes, relays or mirrors for a single group or actor by storing each known location within a list.

| location                 | function    |
|--------------------------|-------------|
| [normalised](normalised) | parsed victim lists |
| [source](source)         | raw/source html |

### GitHub Action

[torproxy](https://github.com/thetanz/gotham) from the [**thetanz/gotham** registry](https://github.com/thetanz/gotham/pkgs/container/gotham%2Ftorproxy) exposes a tor SOCKS5 proxy to the GitHub Action through the use of a [Service Container](https://docs.github.com/en/actions/guides/about-service-containers)

The GitHub Action runs a sequence of commands with ransomwatch.py every 24 hours at 12PM NZDT, updating this repository with findings and optionally sending a report to ms Teams on new posts.

![7B410D65-5B69-4470-ABF5-E31265306293](https://user-images.githubusercontent.com/17993143/130734538-99d8a8ba-7e03-4df3-8360-7e46a676afdd.jpeg)

## Usage

_requires a local tor circuit on tcp://9050_

    docker run -p9050:9050 ghcr.io/thetanz/gotham/torproxy:latest

## Command Line Operations

### Group Tracking

_manage the groups within [groups.json](groups.json)_

#### add new group

    ransomwhere.py add --name acmecorp --location abcdefg.onion

#### add new mirror for an existing group

    ransomwhere.py append --name acmecorp --location abcdefghigklmnop.onion

### scraper

iterates any v3 onion addressses within [groups.json](groups.json), scraping raw HTML (no headless browsers or javascript processing) into [`source/`](source)

    ransomwhere.py scrape

### parser

iterate files within the `source/` directory and append to victim lists within [`normalised/`](normalised)

> postprocessing is done with a mix of `grep`, `awk` and `sed` (see [tools.sh](tools.sh)). It's brittle and like most  ̴̭́H̶̤̓T̸̙̅M̶͇̾L̷͑ͅ ̴̙̏p̸̡͆a̷̛̦r̵̬̿s̴̙͛ĩ̴̺n̸̔͜g̸̘̈, has a limited lifetime.

    ransomwhere.py parse

### reporter

Summary reports (new victims since the previous scrape action) can be sent as [Adaptive Cards](https://adaptivecards.io) to a [Microsoft Teams Webhook](https://docs.microsoft.com/en-us/microsoftteams/platform/webhooks-and-connectors/how-to/add-incoming-webhook)

    ransomwhere.py report --webhookuri https://your-msteams-webhook

If you're not running this locally, you might want to avoid having your webhook location exposed.

> Set this up by forking this repository and [adding a repository secret](https://docs.github.com/en/actions/reference/encrypted-secrets#creating-encrypted-secrets-for-a-repository) named `MSTEAMS_WEBHOOK_URI` with the location of your webhook for the GitHub Action to access. 

> The [GitHub CLI](https://github.com/cli/cli) can be used to add this with `gh secret set MSTEAMS_WEBHOOK_URI --repos ransomwatch`

---

[Theta](https://theta.co.nz)
