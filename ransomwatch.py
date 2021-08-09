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
    providerdict = sharedutils.openjson("groups.json")
    newprovider = createrec(name, location)
    providerdict.extend(newprovider)
    print(json.dumps(providerdict))

def checkExisting(provider):
    groups = sharedutils.openjson("groups.json")
    for group in groups:
        if group['name'] == provider:
            return True
    return False

def scraper():
    groups = sharedutils.openjson("groups.json")
    # iterate each provider
    for group in groups:
        # iterate each location we know about
        for host in group['locations']:
            host['available'] = bool()
            # we can only scrape onion v3, july 2021
            if host['version'] >= 3:
                print(group['name'])
                # make a request through the established tor circuit
                try:
                    response = requests.get(host['slug'], proxies=proxies, headers=headers)
                    filename = group['name'] + '-' + sharedutils.striptld(host['slug']) + '.html'
                    name = os.path.join(os.getcwd(), 'source', filename)
                    file = open(name, "w+")
                    file.write(response.text)
                    file.close()
                    host['available'] = True
                    host['title'] = sharedutils.getsitetitle(name)
                    host['slug'] = response.url
                    host['lastscrape'] = str(datetime.today())
                except requests.exceptions.Timeout as ret:
                    print('failed scrape - connection timeout : ' + group['name'] + ' [' + host['slug'] + ']')
                except requests.exceptions.ConnectionError as rec:
                    print('failed scrape - connection error : ' + group['name'] + ' [' + host['slug'] + ']')
            host['updated'] = str(datetime.today())
            with open('groups.json', 'w', encoding='utf-8') as f:
                json.dump(groups, f, ensure_ascii=False, indent=4)

def reporter():
    diffs = sharedutils.runshellcmd('git diff --name-only normalised/ | cat')
    adaptivecard = sharedutils.openjson("assets/adaptivecard.json")
    if diffs != ([''] or []):
        adaptivecard['body'][1]['columns'][1]['items'][1]['text'] = str(datetime.today())
        for diff in diffs:
            print(diff)
            files = diff.split('/')[1].split('\n')
            for file in files:
                group = file.split('.')[0]
                victims = sharedutils.runshellcmd('git diff main --no-ext-diff --unified=0 --exit-code -a --no-prefix normalised/' + file + ' | egrep "^\+" | sed "/^+++/d" | cut -d "+" -f2')
                vicstring = "\n".join(victims)
                grouphits = sharedutils.composecarditem(group, vicstring)
                adaptivecard['body'].append(grouphits)
        webhookdata = sharedutils.makewebhook(adaptivecard)
        requests.post(args.webhookuri, json=webhookdata)
    else: 
        print('no new orgs to report')

def adder(name, location):
    if checkExisting(name):
        print('records for ' + name + ' already exist, appending to avoid duplication')
        appender(args.name, args.location)
    else:
        groups = sharedutils.openjson("groups.json")
        newrec = createrec(name, location)
        groups.append(dict(newrec))
        with open('groups.json', 'w', encoding='utf-8') as f:
            json.dump(groups, f, ensure_ascii=False, indent=4)

def appender(name, location):
    groups = sharedutils.openjson("groups.json")
    success = bool()
    for group in groups:
        if group['name'] == name:
            group['locations'].append(sharedutils.siteschema(location))
            success = True
    if success:
        with open('groups.json', 'w', encoding='utf-8') as f:
            json.dump(groups, f, ensure_ascii=False, indent=4)
    else:
        print('cannot append to non-existing provider, ' + name)

def lister():
    groups = sharedutils.openjson("groups.json")
    for group in groups:
        for host in group['locations']:
            print(group['name'] + ' - ' + host['slug'])

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
