![](https://avatars0.githubusercontent.com/u/2897191?s=90&v=4)

# ransomwatch 👀 🦅

An onionsite scraping framework, built to watch and track ransomware blogs.

[![ransomwatch](https://github.com/thetanz/ransomwatch/actions/workflows/ransomwatch.yml/badge.svg)](https://github.com/thetanz/ransomwatch/actions/workflows/ransomwatch.yml) [![ransomwatch-build/](https://github.com/thetanz/ransomwatch/actions/workflows/ransomwatch-build.yml/badge.svg)](https://github.com/thetanz/ransomwatch/actions/workflows/ransomwatch-build.yml)

## Technicals

The `groups.json` dictionary handles multiple nodes, relays or mirrors for a single group by storing each known location within a list.

| location                 | function    |
|--------------------------|-------------|
| [normalised](normalised) | raw html    |
| [source](source)         | parsed html |

### GitHub Action

The [torproxy](https://github.com/thetanz/coretools) from the [**thetanz/coretools** registry](https://github.com/thetanz/coretools/pkgs/container/coretools%2Ftorproxy) exposes a tor SOCKS5 proxy to the GitHub Action through the use of a [Service Container](https://docs.github.com/en/actions/guides/about-service-containers)

The GitHub Action runs every 24 hours at 12PM NZDT, updating this repository with findings. 

## Usage

_requires a local tor circuit on tcp://9050_

    docker run -p9050:9050 ghcr.io/thetanz/coretools/torproxy:latest

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
