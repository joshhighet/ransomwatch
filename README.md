![](https://avatars0.githubusercontent.com/u/2897191?s=90&v=4)

# ransomwatch 👀 🦅


## Technical 

We use the [torproxy](https://github.com/thetanz/coretools) from the [**thetanz/coretools** registry](https://github.com/thetanz/coretools/pkgs/container/coretools%2Ftorproxy) to expose a tor SOCKS5 proxy to the GitHub Action through the use of a [Service Container](https://docs.github.com/en/actions/guides/about-service-containers)

This iterates any v3 onion addressses within [gangs.json](gangs.json), scraping raw HTML (there's no headless browser or JS processing involved, so no CAPTCHA bypassing)

The HTML parsing is done with a mix of `grep`, `awk` and `sed`. It's brittle and like any HTML parsing, has a limited lifetime.

Once the HTML is parsed, deduplicated lists are built and can be found within the `normalised/` directory

The `gangs.json` dictionary handles multiple nodes, relays or mirror for a single group by storing each known location within a list and the CLI supports easy additions of new relays and groups

The GitHub Action runs every 24 hours at 12PM NZDT, updating this repository with findings. 

Summary reports can be sent as [Adaptive Cards](https://adaptivecards.io) to a [Microsoft Teams Webhook](https://docs.microsoft.com/en-us/microsoftteams/platform/webhooks-and-connectors/how-to/add-incoming-webhook) by forking this repository and settings the `MSTEAMS_WEBHOOK_URI` secret for the GitHub Action to access. 

## Usage

:bulb: *if running this locally, you'll need to establish a local tor circuit on tcp://9050* :bulb:

    docker run -p9050:9050 ghcr.io/thetanz/coretools/torproxy:latest

### Command Line Operations

### scraper

iterate each gang using a torsocks proxy, saving the raw HTML within the `source/` directory

    ransomwhere.py scrape

### parser

iterate files within the `source/` directory placing vistims within `normalised/`

    ransomwhere.py parse

### add new gang to watchlist

    ransomwhere.py add --name acmecorp --location abcdefg.onion

### add new mirror for existing gang to watchlist

    ransomwhere.py append --name acmecorp --location abcdefghigklmnop.onion

---

[Theta](https://theta.co.nz)
