#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import socket
import codecs
import random
import requests
import lxml.html
import tldextract
import subprocess
'''
we use socks5h to route dns through the socks proxy
this reduces the risk of dns leaks and allows hidden service resolutions
'''
proxies = {
    'http':  'socks5h://127.0.0.1:9050',
    'https': 'socks5h://127.0.0.1:9050'
}

def siteschema(location):
    if not location.startswith('http'):
        location = 'http://' + location
    schema = {
        'fqdn': getapex(location),
        'title': None,
        'version': getonionversion(location)[0],
        'slug': location,
        'meta': None,
        'available': None,
        'updated': None,
        'lastscrape': None,
    }
    return schema

def makewebhook(adaptivecard):
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
    return webhook

def composecarditem(groupname, victims):
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
    return groupitem

def runshellcmd(cmd):
    cmdout = subprocess.run(
        cmd, 
        shell=True, 
        universal_newlines=True, 
        check=True, 
        stdout=subprocess.PIPE
        )
    response = cmdout.stdout.strip().split('\n')
    return response

def headers():
    agents = open('assets/useragents.txt').read().splitlines()
    randomagent = random.choice(agents)
    headers = {'User-Agent': str(randomagent)}
    return headers

def getsitetitle(html) -> str:
    try:
        title = lxml.html.parse(html)
        titletext = title.find(".//title").text
    except AssertionError:
        return None
    return titletext

def hasprotocol(slug):
    return slug.startswith('http')

def getapex(slug):
    stripurl = tldextract.extract(slug)
    return stripurl.domain + '.' + stripurl.suffix

def striptld(slug):
    stripurl = tldextract.extract(slug)
    return stripurl.domain

def gethtml(url):
    return requests.get(url, headers=headers, proxies=proxies).text

def getonionversion(slug):
    version = None
    stripurl = tldextract.extract(slug)
    location = stripurl.domain + '.' + stripurl.suffix
    if len(stripurl.domain) == 16:
        version = 2
    elif len(stripurl.domain) == 56:
        version = 3
    return version, location

def openhtml(file):
    file = codecs.open(file, 'r', 'utf-8')
    return file.read()

def openjson(file):
    with open(file) as f:
        data = json.load(f)
    return data

def checktcp(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('127.0.0.1',port))
    sock.close()
    if result == 0:
        return True
    else:
        return False