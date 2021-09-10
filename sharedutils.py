#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
collection of shared modules used throughout ransomwatch
'''
import sys
import json
import socket
import codecs
import random
import logging
import requests
import lxml.html
import tldextract
import subprocess
from datetime import datetime
from datetime import timedelta
import plotly.graph_objects as go

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
    logging.error(msg)

def honk(msg):
    '''critical error logging with termination'''
    logging.critical(msg)
    sys.exit()

def currentmonthstr():
    months = [
            "january",
            "febuary",
            "march",
            "april",
            "may",
            "june",
            "july",
            "august",
            "september",
            "october",
            "november",
            "december"
        ]
    now = (datetime.now())
    month = (months[now.month])
    return month

'''
socks5h:// ensures we route dns requests through the socks proxy
reduces the risk of dns leaks & allows us to resolve hidden services
'''

oproxies = {
    'http':  'socks5h://' + str(sockshost) + ':' + str(socksport),
    'https': 'socks5h://' + str(sockshost) + ':' + str(socksport)
}

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
    headers = {'User-Agent': str(randomagent())}
    return headers

def socksfetcher(url):
    '''
    fetch a url via socks proxy
    '''
    try:
        stdlog('sharedutils: ' + 'starting socks request to ' + str(url))
        request = requests.get(url, proxies=oproxies, headers=headers())
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
    except requests.exceptions.Timeout as ret:
        errlog('sharedutils: ' + 'socks request timeout - ' + str(ret))
        return None
    except requests.exceptions.ConnectionError as rec:
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
        'available': None,
        'updated': None,
        'lastscrape': None
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
    # limit title text to 20 chars
    if len(titletext) > 20:
        titletext = titletext[:20]
    return titletext

def hasprotocol(slug):
    '''
    checks if a url begins with http - cheap protocol check before we attampt to fetch a page
    '''
    return bool(slug.startswith('http'))

def getapex(slug):
    '''
    returns the apex domain for a given webpage/url slug
    '''
    stripurl = tldextract.extract(slug)
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
    return version, location

def openhtml(file):
    '''
    opens a file and returns the html
    '''
    file = codecs.open(file, 'r', 'utf-8')
    return file.read()

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

def makewebhook(adaptivecard):
    '''
    creates a universal webhook for the msft adaptive card
    https://adaptivecards.io
    '''
    webhook = {
        'type': 'message',
        'attachments': [
            {
            'contentType': 'application/vnd.microsoft.card.adaptive',
            'contentUrl': None,
            'content': adaptivecard
            }
        ]
    }
    dbglog('sharedutils: ' + 'composed webhook - ' + str(webhook))
    return webhook

def composecarditem(groupname, victims):
    '''
    create the card for the adaptive card webhook
    '''
    groupitem = {
        'type': 'ColumnSet',
        'columns': [
            {
                'type': 'Column',
                'width': 'auto',
                'items': [
                    {
                        'type': 'TextBlock',
                        'text': groupname,
                        'wrap': True,
                        'weight': 'Bolder'
                    }
                ]
            },
            {
                'type': 'Column',
                'width': 'stretch',
                'items': [
                    {
                        'type': 'RichTextBlock',
                        'inlines': [
                            {
                                'type': 'TextRun',
                                'text': victims
                            }
                        ]
                    }
                ]
            }
        ]
    }
    dbglog('sharedutils: ' + 'composed card item - ' + str(groupitem))
    return groupitem

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

def geckocount():
    groups = openjson('groups.json')
    gecko_count = 1
    for group in groups:
        if group['geckodriver'] is True:
            gecko_count += 1
    return gecko_count

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

def mounthlypostcount():
    '''
    returns the number of posts within the current month
    '''
    post_count = 0
    posts = openjson('posts.json')
    current_month = datetime.now().month
    for post in posts:
        datetime_object = datetime.strptime(post['discovered'], '%Y-%m-%d %H:%M:%S.%f')
        if datetime_object.month == current_month:
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

def offlinegroups24h():
    '''returns the number of groups that have been offline for the last 24 hours'''
    groups = openjson('groups.json')
    offline_groups = []
    for group in groups:
        for host in group['locations']:
            if host['available'] is False:
                if datetime.now() - datetime.strptime(host['lastscrape'], '%Y-%m-%d %H:%M:%S.%f') > timedelta(hours=24):
                    offline_groups.append(group['name'])
    return offline_groups

def countcaptchahosts():
    '''returns a count on the number of groups that have captchas'''
    groups = openjson('groups.json')
    captcha_count = 0
    for group in groups:
        if group['captcha'] is True:
            captcha_count += 1
    return captcha_count

'''graphs'''

def groupreportpie():
    '''
    create a pie to show the number of posts by each group
    '''
    posts = openjson('posts.json')
    # count the number of posts by group_name within posts.json
    group_counts = {}
    for post in posts:
        if post['group_name'] in group_counts:
            group_counts[post['group_name']] += 1
        else:
            group_counts[post['group_name']] = 1
    # sort the group_counts - descending
    sorted_group_counts = sorted(group_counts.items(), key=lambda x: x[1], reverse=True)
    labels = []
    values = []
    for group in sorted_group_counts:
        labels.append(group[0])
        values.append(group[1])
    fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
    fig.update_layout(title_text='posts by group')
    fig.write_image('docs/postsbygroup.png')

def groupreportmonthly():
    '''chart with plotly the posts by month'''
    posts = openjson('posts.json')
    # count the number of posts by group_name within posts.json
    group_counts = {}
    for post in posts:
        if post['group_name'] in group_counts:
            group_counts[post['group_name']] += 1
        else:
            group_counts[post['group_name']] = 1
    # sort the group_counts - descending
    sorted_group_counts = sorted(group_counts.items(), key=lambda x: x[1], reverse=True)
    # create a list of months
    months = []
    for post in posts:
        if post['discovered'].split(' ')[0] not in months:
            months.append(post['discovered'].split(' ')[0])
    # create a list of months with counts
    month_counts = []
    for month in months:
        month_counts.append([month, 0])
    # count the number of posts by group_name within posts.json
    for post in posts:
        for month in month_counts:
            if post['discovered'].split(' ')[0] == month[0]:
                month[1] += 1
    # sort the month_counts - descending
    sorted_month_counts = sorted(month_counts, key=lambda x: x[1], reverse=True)
    # create a list of months
    labels = []
    for month in sorted_month_counts:
        labels.append(month[0])
    # create a list of counts
    values = []
    for month in sorted_month_counts:
        values.append(month[1])
    fig = go.Figure(data=[go.Bar(x=labels, y=values)])
    fig.update_layout(title_text='posts by month')
    fig.write_image('docs/postsbymonth.png')

def groupreportyearly():
    '''
    chart with plotly the posts by year
    '''
    posts = openjson('posts.json')
    # count the number of posts by group_name within posts.json
    group_counts = {}
    for post in posts:
        if post['group_name'] in group_counts:
            group_counts[post['group_name']] += 1
        else:
            group_counts[post['group_name']] = 1
    # sort the group_counts - descending
    sorted_group_counts = sorted(group_counts.items(), key=lambda x: x[1], reverse=True)
    # create a list of years
    years = []
    for post in posts:
        if post['discovered'].split(' ')[0].split('-')[0] not in years:
            years.append(post['discovered'].split(' ')[0].split('-')[0])
    # create a list of years with counts
    year_counts = []
    for year in years:
        year_counts.append([year, 0])
    # count the number of posts by group_name within posts.json
    for post in posts:
        for year in year_counts:
            if post['discovered'].split(' ')[0].split('-')[0] == year[0]:
                year[1] += 1
    # sort the year_counts - descending
    sorted_year_counts = sorted(year_counts, key=lambda x: x[1], reverse=True)
    # create a list of years
    labels = []
    for year in sorted_year_counts:
        labels.append(year[0])
    # create a list of counts
    values = []
    for year in sorted_year_counts:
        values.append(year[1])
    fig = go.Figure(data=[go.Bar(x=labels, y=values)])
    fig.update_layout(title_text='posts by year')
    fig.write_image('docs/postsbyyear.png')