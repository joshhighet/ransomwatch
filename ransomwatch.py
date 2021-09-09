#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
🧅 👀 🦅 👹
ransomwatch 
does what it says on the tin
'''
import os
import json
import requests
import argparse
from datetime import datetime
# local imports
import parsers
import geckodrive
from sharedutils import striptld
from sharedutils import openjson
from sharedutils import checktcp
from sharedutils import siteschema
from sharedutils import runshellcmd
from sharedutils import makewebhook
from sharedutils import socksfetcher
from sharedutils import getsitetitle
from sharedutils import getonionversion
from sharedutils import composecarditem
from sharedutils import sockshost, socksport
from sharedutils import stdlog, dbglog, errlog, honk

print(
    '''
       _______________                        |*\_/*|________
      |  ___________  |                      ||_/-\_|______  |
      | |           | |                      | |           | |
      | |   0   0   | |                      | |   0   0   | |
      | |     -     | |                      | |     -     | |
      | |   \___/   | |                      | |   \___/   | |
      | |___     ___| |                      | |___________| |
      |_____|\_/|_____|                      |_______________|
        _|__|/ \|_|_.............💔.............._|________|_
       / ********** \                          / ********** \ 
     /  ************  \     ransomwhat?      /  ************  \ 
    --------------------                    --------------------
    '''
)

parser = argparse.ArgumentParser(description='👀 🦅 ransomwatch')
parser.add_argument("--name", help='provider name')
parser.add_argument("--location", help='onionsite fqdn')
parser.add_argument("--webhookuri", help='uri of microsoft teams webhook for reporting')
parser.add_argument("--append", help='add onionsite fqdn to existing record')
parser.add_argument(
    "mode",
    help='operation to execute',
    choices=['add', 'append', 'scrape', 'parse', 'list', 'report']
    )
args = parser.parse_args()

if args.mode == ('add' or 'append') and (args.name is None or args.location is None):
    parser.error("operation requires --name and --location")

if args.location:
    siteinfo = getonionversion(args.location)
    if siteinfo[0] is None:
        parser.error("location does not appear to be a v2 or v3 onionsite")
    location = siteinfo[1]

if args.mode == 'report' and args.webhookuri is None:
    parser.error("operation requires --webhookuri")

def creategroup(name, location):
    '''
    create a new group for a new provider - added to groups.json
    '''
    location = siteschema(location)
    insertdata = {
        'name': name,
        'parser': bool(),
        'geckodriver': bool(),
        'locations': [
            location
        ]
    }
    return insertdata

def checkexisting(provider):
    '''
    check if group already exists within groups.json
    '''
    groups = openjson("groups.json")
    for group in groups:
        if group['name'] == provider:
            return True
    return False

def scraper():
    '''main scraping function'''
    groups = openjson("groups.json")
    # iterate each provider
    for group in groups:
        stdlog('ransomwatch: ' + 'working on ' + group['name'])
        # iterate each location/mirror/relay
        for host in group['locations']:
            stdlog('ransomwatch: ' + 'scraping ' + host['slug'])
            host['available'] = bool()
            '''
            we can only scrape onion v3, july 2021
            https://support.torproject.org/onionservices/v2-deprecation/
            '''
            if host['version'] >= 3:
                if group['geckodriver'] is True:
                    stdlog('ransomwatch: ' + 'using geckodriver')
                    response = geckodrive.main(host['slug'])
                elif group['geckodriver'] is False:
                    stdlog('ransomwatch: ' + 'using socksfetcher')
                    response = socksfetcher(host['slug'])
                
                if response is not None:
                    stdlog('ransomwatch: ' + 'scraping ' + host['slug'] + ' successful')
                    filename = group['name'] + '-' + striptld(host['slug']) + '.html'
                    name = os.path.join(os.getcwd(), 'source', filename)
                    stdlog('ransomwatch: ' + 'saving ' + name)
                    with open(name, 'w', encoding='utf-8') as sitesource:
                        sitesource.write(response)
                        sitesource.close()
                    dbglog('ransomwatch: ' + 'saving ' + name + ' successful')
                    
                    host['available'] = True
                    host['title'] = getsitetitle(name)
                    host['lastscrape'] = str(datetime.today())            
                    host['updated'] = str(datetime.today())
                    dbglog('ransomwatch: ' + 'scrape successful')
                    with open('groups.json', 'w', encoding='utf-8') as f:
                        json.dump(groups, f, ensure_ascii=False, indent=4)

def reporter():
    '''
    main report function to notify on differentials
    '''
    diffs = runshellcmd('git diff --name-only normalised/ | cat')
    adaptivecard = openjson("assets/adaptivecard.json")
    if diffs != ([''] or []):
        adaptivecard['body'][1]['columns'][1]['items'][1]['text'] = str(datetime.today())
        for diff in diffs:
            files = diff.split('/')[1].split('\n')
            for file in files:
                group = file.split('.')[0]
                victims = runshellcmd('git diff main --no-ext-diff --unified=0 --exit-code -a --no-prefix normalised/' + file + ' | egrep "^\+" | sed "/^+++/d" | cut -d "+" -f2')
                vicstring = "\n".join(victims)
                grouphits = composecarditem(group, vicstring)
                adaptivecard['body'].append(grouphits)
        webhookdata = makewebhook(adaptivecard)
        requests.post(args.webhookuri, json=webhookdata)
    else:
        pass

def adder(name, location):
    '''
    handles the addition of new providers to groups.json
    '''
    if checkexisting(name):
        stdlog('ransomwatch: ' + 'records for ' + name + ' already exist, appending to avoid duplication')
        appender(args.name, args.location)
    else:
        groups = openjson("groups.json")
        newrec = creategroup(name, location)
        groups.append(dict(newrec))
        with open('groups.json', 'w', encoding='utf-8') as groupsfile:
            json.dump(groups, groupsfile, ensure_ascii=False, indent=4)
        stdlog('ransomwatch: ' + 'record for ' + name + ' added to groups.json')

def appender(name, location):
    '''
    handles the addition of new mirrors and relays for the same site
    to an existing group within groups.json
    '''
    groups = openjson("groups.json")
    success = bool()
    for group in groups:
        if group['name'] == name:
            group['locations'].append(siteschema(location))
            success = True
    if success:
        with open('groups.json', 'w', encoding='utf-8') as groupsfile:
            json.dump(groups, groupsfile, ensure_ascii=False, indent=4)
    else:
        honk('cannot append to non-existing provider, ' + name)

def lister():
    '''
    basic function to list out providers &  their addresses to a terminal
    '''
    groups = openjson("groups.json")
    for group in groups:
        for host in group['locations']:
            print(group['name'] + ' - ' + host['slug'])

if args.mode == 'scrape':
    '''check we have a socks proxy available for us - call the scraper to commence if we do'''
    if not checktcp(sockshost, socksport):
        honk("socks proxy not available and required for scraping!")
    scraper()

if args.mode == 'add':
    adder(args.name, args.location)

if args.mode == 'append':
    appender(args.name, args.location)

if args.mode == 'report':
    reporter()

if args.mode == 'parse':
    parsers.synack()
    parsers.suncrypt()
    parsers.lorenz()
    parsers.lockbit2()
    parsers.arvinclub()
    parsers.avoslocker()
    parsers.avaddon()
    parsers.xinglocker()
    parsers.ragnarlocker()
    parsers.clop()
    parsers.revil()
    parsers.ragnarok()
    parsers.conti()
    parsers.pysa()
    parsers.nefilim()
    parsers.mountlocker()
    parsers.babuklocker()
    parsers.ransomexx()
    parsers.cuba()
    parsers.pay2key()
    parsers.azroteam()
    parsers.lockdata()
    parsers.blacktor()
    parsers.darkleakmarket()
    parsers.blackmatter()
    parsers.payloadbin()
    parsers.groove()

if args.mode == 'list':
    lister()
