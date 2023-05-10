#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
collection of shared modules used throughout ransomwatch
'''
import os
import sys
import json
import socket
import codecs
import random
import logging
from datetime import datetime
from datetime import timedelta
import subprocess
import tldextract
import lxml.html
import requests

sockshost = '127.0.0.1'
socksport = 9050

logging.basicConfig(
    format='%(asctime)s,%(msecs)d %(levelname)-8s %(message)s',
    datefmt='%Y-%m-%d:%H:%M:%S',
    level=logging.INFO
    )

def stdlog(msg):
    '''standard infologging'''
    logging.info(msg)

def dbglog(msg):
    '''standard debug logging'''
    logging.debug(msg)

def errlog(msg):
    '''standard error logging'''
    logging.error(msg)

def honk(msg):
    '''critical error logging with termination'''
    logging.critical(msg)
    sys.exit()

def currentmonthstr():
    '''
    return the current, full month name in lowercase
    '''
    return datetime.now().strftime('%B').lower()

# socks5h:// ensures we route dns requests through the socks proxy
# reduces the risk of dns leaks & allows us to resolve hidden services

oproxies = {
    'http':  'socks5h://' + str(sockshost) + ':' + str(socksport),
    'https': 'socks5h://' + str(sockshost) + ':' + str(socksport)
}

def checkgeckodriver():
    '''
    check if geckodriver is in the system $PATH
    '''
    stdlog('sharedutils: ' + 'checking if geckodriver is in $PATH')
    cmd = 'geckodriver --version'
    try:
        output = runshellcmd(cmd)
        if 'geckodriver' in output[0]:
            stdlog('sharedutils: ' + 'geckodriver is in $PATH')
            return True
        errlog('sharedutils: ' + 'geckodriver is not in $PATH')
        return False
    except subprocess.CalledProcessError as cpe:
        errlog('sharedutils: ' + 'geckodriver check failed - ' + str(cpe))
        return False

def randomagent():
    '''
    randomly return a useragent from assets/useragents.txt
    '''
    with open('assets/useragents.txt', encoding='utf-8') as uafile:
        uas = uafile.read().splitlines()
        uagt = random.choice(uas)
        dbglog('sharedutils: ' + 'random user agent - ' + str(uagt))
    return uagt

def headers():
    '''
    returns a key:val user agent header for use with the requests library
    '''
    headerstr = {'User-Agent': str(randomagent())}
    return headerstr

def metafetch(url):
    '''
    return the status code & http server using oproxies and headers
    '''
    try:
        stdlog('sharedutils: ' + 'meta prefetch request to ' + str(url))
        request = requests.head(url, proxies=oproxies, headers=headers(), timeout=20)
        statcode = request.status_code
        try:
            response = request.headers['server']
            return statcode, response
        except KeyError as ke:
            errlog('sharedutils: ' + 'meta prefetch did not discover server - ' + str(ke))
            return statcode, None
    except requests.exceptions.Timeout as ret:
        errlog('sharedutils: ' + 'meta request timeout - ' + str(ret))
        return None, None
    except requests.exceptions.ConnectionError as rec:
        errlog('sharedutils: ' + 'meta request connection error - ' + str(rec))
        return None, None

def socksfetcher(url):
    '''
    fetch a url via socks proxy
    '''
    try:
        stdlog('sharedutils: ' + 'starting socks request to ' + str(url))
        request = requests.get(url, proxies=oproxies, headers=headers(), timeout=20, verify=False)
        dbglog(
            'sharedutils: ' + 'socks request - recieved statuscode - ' \
                + str(request.status_code)
            )
        try:
            response = request.text
            return response
        except AttributeError as ae:
            errlog('sharedutils: ' + 'socks response error - ' + str(ae))
            return None
    except requests.exceptions.Timeout:
        errlog('geckodriver: ' + 'socks request timed out!')
        return None
    except requests.exceptions.ConnectionError as rec:
        # catch SOCKSHTTPConnectionPool Host unreachable
        if 'SOCKSHTTPConnectionPool' and 'Host unreachable' in str(rec):
            errlog('sharedutils: ' + 'socks request unable to route to host, check hsdir resolution status!')
            return None
        errlog('sharedutils: ' + 'socks request connection error - ' + str(rec))
        return None

def siteschema(location):
    '''
    returns a dict with the site schema
    '''
    if not location.startswith('http'):
        dbglog('sharedutils: ' + 'assuming we have been given an fqdn and appending protocol')
        location = 'http://' + location
    schema = {
        'fqdn': getapex(location),
        'title': None,
        'version': getonionversion(location)[0],
        'slug': location,
        'available': False,
        'updated': None,
        'lastscrape': '2021-05-01 00:00:00.000000',
        'enabled': True
    }
    dbglog('sharedutils: ' + 'schema - ' + str(schema))
    return schema

def runshellcmd(cmd):
    '''
    runs a shell command and returns the output
    '''
    stdlog('sharedutils: ' + 'running shell command - ' + str(cmd))
    cmdout = subprocess.run(
        cmd,
        shell=True,
        universal_newlines=True,
        check=True,
        stdout=subprocess.PIPE
        )
    response = cmdout.stdout.strip().split('\n')
    # if empty list output, error
    # if len(response) == 1:
    #     honk('sharedutils: ' + 'shell command returned no output')
    return response

def getsitetitle(html) -> str:
    '''
    tried to parse out the title of a site from the html
    '''
    stdlog('sharedutils: ' + 'getting site title')
    try:
        title = lxml.html.parse(html)
        titletext = title.find(".//title").text
    except AssertionError:
        stdlog('sharedutils: ' + 'could not fetch site title from source - ' + str(html))
        return None
    except AttributeError:
        stdlog('sharedutils: ' + 'could not fetch site title from source - ' + str(html))
        return None
    # limit title text to 50 chars
    if titletext is not None:
        if len(titletext) > 50:
            titletext = titletext[:50]
        stdlog('sharedutils: ' + 'site title - ' + str(titletext))
        return titletext
    stdlog('sharedutils: ' + 'could not find site title from source - ' + str(html))
    return None

def gcount(posts):
    group_counts = {}
    for post in posts:
        if post['group_name'] in group_counts:
            group_counts[post['group_name']] += 1
        else:
            group_counts[post['group_name']] = 1
    return group_counts

def hasprotocol(slug):
    '''
    checks if a url begins with http - cheap protocol check before we attampt to fetch a page
    '''
    return bool(slug.startswith('http'))

def getapex(slug):
    '''
    returns the domain for a given webpage/url slug
    '''
    stripurl = tldextract.extract(slug)
    print(stripurl)
    if stripurl.subdomain:
        return stripurl.subdomain + '.' + stripurl.domain + '.' + stripurl.suffix
    return stripurl.domain + '.' + stripurl.suffix

def striptld(slug):
    '''
    strips the tld from a url
    '''
    stripurl = tldextract.extract(slug)
    return stripurl.domain

def getonionversion(slug):
    '''
    returns the version of an onion service (v2/v3)
    https://support.torproject.org/onionservices/v2-deprecation
    '''
    version = None
    stripurl = tldextract.extract(slug)
    location = stripurl.domain + '.' + stripurl.suffix
    stdlog('sharedutils: ' + 'checking for onion version - ' + str(location))
    if len(stripurl.domain) == 16:
        stdlog('sharedutils: ' + 'v2 onionsite detected')
        version = 2
    elif len(stripurl.domain) == 56:
        stdlog('sharedutils: ' + 'v3 onionsite detected')
        version = 3
    else:
        stdlog('sharedutils: ' + 'unknown onion version, assuming clearnet')
        version = 0
    return version, location

def openhtml(file):
    '''
    opens a file and returns the html
    '''
    with open(file, 'r', encoding='utf-8') as f:
        html = f.read()
    return html

def openjson(file):
    '''
    opens a file and returns the json as a dict
    '''
    with open(file, encoding='utf-8') as jsonfile:
        data = json.load(jsonfile)
    return data

def checktcp(host, port):
    '''
    checks if a tcp port is open - used to check if a socks proxy is available
    '''
    stdlog('sharedutils: ' + 'attempting socket connection')
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex((str(host), int(port)))
    sock.close()
    if result == 0:
        stdlog('sharedutils: ' + 'socket - successful connection')
        return True
    stdlog('sharedutils: ' + 'socket - failed connection')
    return False

def postcount():
    post_count = 1
    posts = openjson('posts.json')
    for post in posts:
        post_count += 1
    return post_count

def groupcount():
    groups = openjson('groups.json')
    return len(groups)

def parsercount():
    groups = openjson('groups.json')
    parse_count = 1
    for group in groups:
        if group['parser'] is True:
            parse_count += 1
    return parse_count

def hostcount():
    groups = openjson('groups.json')
    host_count = 0
    for group in groups:
        for host in group['locations']:
            host_count += 1
    return host_count

def headlesscount():
    groups = openjson('groups.json')
    js_count = 0
    for group in groups:
        if group['javascript_render'] is True:
            js_count += 1
    return js_count

def onlinecount():
    groups = openjson('groups.json')
    online_count = 0
    for group in groups:
        for host in group['locations']:
            if host['available'] is True:
                online_count += 1
    return online_count

def version2count():
    groups = openjson('groups.json')
    version2_count = 0
    for group in groups:
        for host in group['locations']:
            if host['version'] == 2:
                version2_count += 1
    return version2_count

def version3count():
    groups = openjson('groups.json')
    version3_count = 0
    for group in groups:
        for host in group['locations']:
            if host['version'] == 3:
                version3_count += 1
    return version3_count

def monthlypostcount():
    '''
    returns the number of posts within the current month
    '''
    post_count = 0
    posts = openjson('posts.json')
    current_month = datetime.now().month
    current_year = datetime.now().year
    for post in posts:
        datetime_object = datetime.strptime(post['discovered'], '%Y-%m-%d %H:%M:%S.%f')
        if datetime_object.year == current_year and datetime_object.month == current_month:
                post_count += 1
    return post_count

def postssince(days):
    '''returns the number of posts within the last x days'''
    post_count = 0
    posts = openjson('posts.json')
    for post in posts:
        datetime_object = datetime.strptime(post['discovered'], '%Y-%m-%d %H:%M:%S.%f')
        if datetime_object > datetime.now() - timedelta(days=days):
            post_count += 1
    return post_count

def poststhisyear():
    '''returns the number of posts within the current year'''
    post_count = 0
    posts = openjson('posts.json')
    current_year = datetime.now().year
    for post in posts:
        datetime_object = datetime.strptime(post['discovered'], '%Y-%m-%d %H:%M:%S.%f')
        if datetime_object.year == current_year:
            post_count += 1
    return post_count

def postslast24h():
    '''returns the number of posts within the last 24 hours'''
    post_count = 0
    posts = openjson('posts.json')
    for post in posts:
        datetime_object = datetime.strptime(post['discovered'], '%Y-%m-%d %H:%M:%S.%f')
        if datetime_object > datetime.now() - timedelta(hours=24):
            post_count += 1
    return post_count

def countcaptchahosts():
    '''returns a count on the number of groups that have captchas'''
    groups = openjson('groups.json')
    captcha_count = 0
    for group in groups:
        if group['captcha'] is True:
            captcha_count += 1
    return captcha_count

def todiscord(post_title, group, hook_uri):
    '''
    sends a post to a discord webhook defined as an envar
    '''
    dbglog('sharedutils: ' + 'sending to discord webhook')
    # avoid json decode errors by escaping the title if contains \ or "
    post_title = post_title.replace('\\', '\\\\').replace('"', '\\"')
    discord_data = '''
    {
        "content": "[**%s**](https://ransomwatch.telemetry.ltd/#/profiles?id=%s) posted `%s`",
        "embeds": null,
        "username": "ransomwatch",
        "avatar_url": "https://github.com/joshhighet/ransomwatch/blob/main/docs/apple-touch-icon.png?raw=true",
        "attachments": [],
        "flags": 4100
    }''' % (group, group, post_title)
    discord_json = json.loads(discord_data)
    stdlog('sharedutils: ' + 'sending to discord webhook')
    dscheaders = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    try:
        hookpost = requests.post(hook_uri, json=discord_json, headers=dscheaders)
    except requests.exceptions.RequestException as e:
        honk('sharedutils: ' + 'error sending to discord webhook: ' + str(e))
    if hookpost.status_code == 204:
        return True
    if hookpost.status_code == 429:
        errlog('sharedutils: ' + 'discord webhook rate limit exceeded')
    else:
        honk('sharedutils: ' + 'recieved discord webhook error resonse ' + str(hookpost.status_code) + ' with text ' + str(hookpost.text))
    return False

def toteams(post_title, group):
    '''
    sends a post to a miCroSoFt tEaMs webhook defined as an envar
    '''
    stdlog('sharedutils: ' + 'sending to microsoft teams webhook')
    # avoid json decode errors by escaping the title if contains \ or "
    post_title = post_title.replace('\\', '\\\\').replace('"', '\\"')
    teams_data = '''
    {
    "type":"message",
    "attachments":[
        {
            "contentType":"application/vnd.microsoft.card.adaptive",
            "contentUrl":null,
            "content":{
                "type": "AdaptiveCard",
                "body": [
                    {
                        "type": "TextBlock",
                        "text": "%s",
                        "isSubtle": true,
                        "wrap": true
                    }
                ],
                "actions": [
                    {
                        "type": "Action.OpenUrl",
                        "title": "%s",
                        "url": "https://ransomwatch.telemetry.ltd/#/profiles?id=%s"
                    }
                ],
                "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                "version": "1.4"
            }
        }
    ]
    }''' % (post_title, group, group)
    try:
        hook_uri = os.environ.get('MS_TEAMS_WEBHOOK')
        hookpost = requests.post(hook_uri, data=teams_data, headers={'Content-Type': 'application/json'})
    except requests.exceptions.RequestException as e:
        honk('sharedutils: ' + 'error sending to microsoft teams webhook: ' + str(e))
    if hookpost.status_code == 200:
        return True
    if hookpost.status_code == 429:
        errlog('sharedutils: ' + 'microsoft teams webhook rate limit exceeded')
    else:
        honk('sharedutils: ' + 'recieved microsoft teams webhook error resonse ' + str(hookpost.status_code) + ' with text ' + str(hookpost.text))
    return False
    