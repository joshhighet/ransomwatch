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
            errlog('sharedutils: ' + 'socks response error - ' + ae)
            return None
    except requests.exceptions.Timeout as ret:
        errlog('sharedutils: ' + 'socks request timeout - ' + ret)
        return None
    except requests.exceptions.ConnectionError as rec:
        errlog('sharedutils: ' + 'socks request connection error - ' + rec)
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
        'meta': None,
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
        return None
    except AttributeError:
        return None
    stdlog('sharedutils: ' + 'site title - ' + str(titletext))
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
