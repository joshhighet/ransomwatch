#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import json
import argparse
import requests
import subprocess
from datetime import datetime
# local imports
import sharedutils

parser = argparse.ArgumentParser()
parser.add_argument("--name", help='provider name')
parser.add_argument("--location", help='onionsite fqdn')
parser.add_argument("--webhookuri", help='uri of microsoft teams webhook for reporting')
parser.add_argument("mode", help='operation to execute', choices=['add', 'append', 'scrape', 'parse', 'list', 'report'])
parser.add_argument("--append", help='add onionsite fqdn to existing record')
args = parser.parse_args()

if args.mode == ('add' or 'append') and (args.name is None or args.location is None):
    parser.error("operation requires --name and --location")

if args.location:
    siteinfo = sharedutils.getonionversion(args.location)
    if siteinfo[0] is None:
        parser.error("location does not appear to be a v2 or v3 onionsite")
    location = siteinfo[1]

if args.mode == 'report' and args.webhookuri is None:
    parser.error("operation requires --webhookuri")

proxies = sharedutils.proxies
headers = sharedutils.headers()


'''
sticking to hacky bash scripts for now on the parsing front.
beautifulsoup would be a cleaner implementation but comes setup grief
######
from bs4 import BeautifulSoup

def soupinit(file):
    htmldoc = sharedutils.openhtml(file)
    soup = BeautifulSoup(htmldoc, 'html.parser')
    return soup

def arvinclub(doc):
    soup = soupinit(doc)
    headers = soup.find_all('h2')
    for head in headers:
        part = str(head).partition('bookmark">')[2]
        title = part.strip('</a></h2>')
        print(title)

arvinclub('source/arvinclub.html')
'''

def createrec(name, location):
    location = sharedutils.siteschema(location)
    insertdata = {
        'name': name,
        'locations': [
            location
        ]
    }
    return insertdata

def insert(name, location):
    providerdict = sharedutils.openjson("gangs.json")
    newprovider = createrec(name, location)
    providerdict.extend(newprovider)
    print(json.dumps(providerdict))

def checkExisting(provider):
    gangs = sharedutils.openjson("gangs.json")
    for gang in gangs:
        if gang['name'] == provider:
            return True
    return False

def scraper():
    gangs = sharedutils.openjson("gangs.json")
    # iterate each provider
    for gang in gangs:
        # iterate each location we know about
        for host in gang['locations']:
            host['available'] = bool()
            # we can only scrape onion v3, july 2021
            if host['version'] >= 3:
                print(gang['name'])
                # make a request through the established tor circuit
                try:
                    response = requests.get(host['slug'], proxies=proxies, headers=headers)
                    filename = gang['name'] + '-' + sharedutils.striptld(host['slug']) + '.html'
                    name = os.path.join(os.getcwd(), 'source', filename)
                    file = open(name, "w+")
                    file.write(response.text)
                    file.close()
                    host['available'] = True
                    host['title'] = sharedutils.getsitetitle(name)
                    host['slug'] = response.url
                    host['lastscrape'] = str(datetime.today())
                except requests.exceptions.Timeout as ret:
                    print('failed scrape - connection timeout : ' + gang['name'] + ' [' + host['slug'] + ']')
                except requests.exceptions.ConnectionError as rec:
                    print('failed scrape - connection error : ' + gang['name'] + ' [' + host['slug'] + ']')
            host['updated'] = str(datetime.today())
            with open('gangs.json', 'w', encoding='utf-8') as f:
                json.dump(gangs, f, ensure_ascii=False, indent=4)

def reporter():
    diffs = sharedutils.runshellcmd('git diff --name-only normalised/ | cat')
    adaptivecard = sharedutils.openjson("assets/adaptivecard.json")
    if diffs != ([''] or []):
        adaptivecard['body'][1]['columns'][1]['items'][1]['text'] = str(datetime.today())
        for diff in diffs:
            files = diff.split('/')[2].split('\n')
            for file in files:
                gang = file.split('.')[0]
                victims = sharedutils.runshellcmd('git diff main --no-ext-diff --unified=0 --exit-code -a --no-prefix normalised/' + file + ' | egrep "^\+" | sed "/^+++/d" | cut -d "+" -f2')
                vicstring = "\n".join(victims)
                ganghits = sharedutils.composecarditem(gang, vicstring)
                adaptivecard['body'].append(ganghits)
        webhookdata = sharedutils.makewebhook(adaptivecard)
        requests.post(args.webhookuri, json=webhookdata)
    else: 
        print('no new orgs to report')

def adder(name, location):
    if checkExisting(name):
        print('records for ' + name + ' already exist, appending to avoid duplication')
        appender(args.name, args.location)
    else:
        gangs = sharedutils.openjson("gangs.json")
        newrec = createrec(name, location)
        gangs.append(dict(newrec))
        with open('gangs.json', 'w', encoding='utf-8') as f:
            json.dump(gangs, f, ensure_ascii=False, indent=4)

def appender(name, location):
    gangs = sharedutils.openjson("gangs.json")
    success = bool()
    for gang in gangs:
        if gang['name'] == name:
            gang['locations'].append(sharedutils.siteschema(location))
            success = True
    if success:
        with open('gangs.json', 'w', encoding='utf-8') as f:
            json.dump(gangs, f, ensure_ascii=False, indent=4)
    else:
        print('cannot append to non-existing provider, ' + name)

def lister():
    gangs = sharedutils.openjson("gangs.json")
    for gang in gangs:
        for host in gang['locations']:
            print(gang['name'] + ' - ' + host['slug'])

def grepper():
    subprocess.call(['./tools.sh', 'parser'])

if args.mode == 'scrape':
    # ensure we have a socks proxy available to us first...
    if not sharedutils.checktcp(9050):
        parser.error("socks proxy not available and required for scraping!")
    scraper()

if args.mode == 'add':
    adder(args.name, args.location)

if args.mode == 'append':
    appender(args.name, args.location)


if args.mode == 'report':
    reporter()

if args.mode == 'parse':
    grepper()

if args.mode == 'list':
    lister()
