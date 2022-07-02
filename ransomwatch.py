#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
🧅 👀 🦅 👹
ransomwatch
does what it says on the tin
'''
import os
import json
import argparse
from datetime import datetime

# local imports

import parsers
import geckodrive
from markdown import main as markdown

from sharedutils import striptld
from sharedutils import openjson
from sharedutils import checktcp
from sharedutils import siteschema
from sharedutils import socksfetcher
from sharedutils import getsitetitle
from sharedutils import getonionversion
from sharedutils import checkgeckodriver
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
parser.add_argument("--append", help='add onionsite fqdn to existing record')
parser.add_argument(
    "mode",
    help='operation to execute',
    choices=['add', 'append', 'scrape', 'parse', 'list', 'markdown', 'check']
    )
args = parser.parse_args()

if args.mode == ('add' or 'append') and (args.name is None or args.location is None):
    parser.error("operation requires --name and --location")

if args.mode == 'check' and args.location is None:
    parser.error("operation requires --location")

if args.location:
    # if args.location ends in .onion
    if args.location.endswith('.onion'):
        siteinfo = getonionversion(args.location)
        if siteinfo[0] is None:
            parser.error("location does not appear to be a v2 or v3 onionsite")
    else:
        errlog("location does not appear to be an onionsite, assuming clearnet")

def creategroup(name, location):
    '''
    create a new group for a new provider - added to groups.json
    '''
    location = siteschema(location)
    insertdata = {
        'name': name,
        'captcha': bool(),
        'parser': bool(),
        'javascript_render': bool(),
        'meta': None,
        'locations': [
            location
        ],
        'profile': list()
    }
    return insertdata

# check if a given location exists in groups.json
if args.mode == 'check':
    groups = openjson("groups.json")
    for group in groups:
        for location in group['locations']:
            if location['fqdn'] == args.location:
                print('ransomwatch: ' + 'location ' + args.location + ' is in groups.json')
                exit()
    print('ransomwatch: ' + 'location ' + args.location + ' is not in groups.json')
    exit()

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
            only scrape onion v3 unless using headless browser, not long before this will not be possible
            https://support.torproject.org/onionservices/v2-deprecation/
            '''
            if host['version'] == 3 or host['version'] == 0:
                if group['javascript_render'] is True:
                    stdlog('ransomwatch: ' + 'using javascript_render (geckodriver)')
                    response = geckodrive.main(host['slug'])
                else:
                    stdlog('ransomwatch: ' + 'using standard socksfetcher')
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
                    with open('groups.json', 'w', encoding='utf-8') as groupsfile:
                        json.dump(groups, groupsfile, ensure_ascii=False, indent=4)
                        groupsfile.close()
                        dbglog('ransomwatch: ' + 'groups.json updated')
                else:
                    errlog('ransomwatch: ' + 'task on ' + group['name'] + ' failed to return a response')
            else:
                errlog('ransomwatch: ' + 'scrape failed - ' + host['slug'] + ' is not a v3 onionsite')

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
        honk('cannot append to non-existing provider')

def lister():
    '''
    basic function to list out groups & addresses to term
    '''
    groups = openjson("groups.json")
    for group in groups:
        for host in group['locations']:
            print(group['name'] + ' - ' + host['slug'])

if args.mode == 'scrape':
    if not checktcp(sockshost, socksport):
        honk("socks proxy not available and required for scraping!")
    if checkgeckodriver() is False:
        honk('ransomwatch: ' + 'geckodriver not found in $PATH and required for scraping')
    scraper()
    stdlog('ransomwatch: ' + 'scrape run complete')

if args.mode == 'add':
    adder(args.name, args.location)

if args.mode == 'append':
    appender(args.name, args.location)

if args.mode == 'markdown':
    markdown()
    stdlog('ransomwatch: ' + 'markdown run complete')

if args.mode == 'parse':
    parsers.suncrypt()
    parsers.bonacigroup()
    parsers.blackbyte()
    parsers.spook()
    parsers.karma()
    parsers.suncrypt()
    parsers.lorenz()
    parsers.lockbit2()
    parsers.arvinclub()
    parsers.avaddon()
    parsers.xinglocker()
    parsers.ragnarlocker()
    parsers.clop()
    parsers.revil()
    parsers.everest()
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
    parsers.quantum()
    parsers.atomsilo()
    parsers.lv()
    parsers.five4bb47h()
    parsers.snatch()
    parsers.midas()
    parsers.marketo()
    parsers.rook()
    parsers.cryp70n1c0d3()
    parsers.hiveleak()
    parsers.mosesstaff()
    parsers.alphv()
    parsers.nightsky()
    parsers.vicesociety()
    parsers.pandora()
    parsers.stormous()
    parsers.leaktheanalyst()
    parsers.kelvinsecurity()
    parsers.blackbasta()
    parsers.onyx()
    parsers.mindware()
    parsers.ransomhouse()
    parsers.cheers()
    parsers.lockbit3()
    parsers.yanluowang()
    stdlog('ransomwatch: ' + 'parse run complete')

if args.mode == 'list':
    lister()
