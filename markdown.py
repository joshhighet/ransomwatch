#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import time
import random
from datetime import datetime as dt

from sharedutils import gcount
from sharedutils import openjson
from sharedutils import postcount
from sharedutils import hostcount
from sharedutils import groupcount
from sharedutils import postssince
from sharedutils import parsercount
from sharedutils import onlinecount
from sharedutils import postslast24h
from sharedutils import headlesscount
from sharedutils import version2count
from sharedutils import poststhisyear
from sharedutils import currentmonthstr
from sharedutils import mounthlypostcount
from sharedutils import countcaptchahosts

from sharedutils import stdlog, dbglog, errlog, honk

from plotting import barchartgroups
from plotting import groupheatmap

def suffix(d):
    return 'th' if 11<=d<=13 else {1:'st',2:'nd',3:'rd'}.get(d%10, 'th')

def custom_strftime(fmt, t):
    return t.strftime(fmt).replace('{S}', str(t.day) + suffix(t.day))

friendly_tz = custom_strftime('%B {S}, %Y', dt.now()).lower()

def writeline(file, line):
    '''write line to file'''
    with open(file, 'a') as f:
        f.write(line + '\n')
        f.close()

def groupreport():
    '''
    create a list with number of posts per unique group
    '''
    stdlog('generating group report')
    posts = openjson('posts.json')
    # count the number of posts by group_name within posts.json
    group_counts = gcount(posts)
    # sort the group_counts - descending
    sorted_group_counts = sorted(group_counts.items(), key=lambda x: x[1], reverse=True)
    stdlog('group report generated with %d groups' % len(sorted_group_counts))
    return sorted_group_counts

def mainpage():
    '''
    main markdown report generator - used with github pages
    '''
    stdlog('generating main page')
    uptime_sheet = 'docs/README.md'
    with open(uptime_sheet, 'w') as f:
        f.close()
    groups = openjson('groups.json')
    writeline(uptime_sheet, '')
    writeline(uptime_sheet, '_:warning: all site pages and graphs are dynamically generated every half hour_')
    writeline(uptime_sheet, '')
    writeline(uptime_sheet, '> see the project [README](https://github.com/thetanz/ransomwatch#ransomwatch--) for technicals')
    writeline(uptime_sheet, '')
    # link to the stats and pfoiles pages
    writeline(uptime_sheet, '## [`stats n\' graphs`](stats.md)')
    writeline(uptime_sheet, '')
    writeline(uptime_sheet, '## [`group profiles`](profiles.md)')
    writeline(uptime_sheet, '')
    writeline(uptime_sheet, '## 📰 summary - ' + friendly_tz)
    writeline(uptime_sheet, '')
    writeline(uptime_sheet, 'currently tracking `' + str(groupcount()) + '` groups across `' + str(hostcount()) + '` various relays and mirrors - ' + '_`' + str(onlinecount()) + '` of which are online_')
    writeline(uptime_sheet, '')
    writeline(uptime_sheet, 'there are `' + str(parsercount()) + '` active parsers, `' + str(headlesscount()) + '` of which using headless browsers - _`' + str(countcaptchahosts()) + '` groups have recently introduced captchas_')
    writeline(uptime_sheet, '')
    writeline(uptime_sheet, '⏲ there have been `' + str(postslast24h()) + '` posts within the `last 24 hours`')
    writeline(uptime_sheet, '')
    writeline(uptime_sheet, '🦈 there have been `' + str(mounthlypostcount()) + '` posts within the `month of ' + currentmonthstr() + '`')
    writeline(uptime_sheet, '')
    writeline(uptime_sheet, '🪐 there have been `' + str(postssince(90)) + '` posts within the `last 90 days`')
    writeline(uptime_sheet, '')
    writeline(uptime_sheet, '🏚 there have been `' + str(poststhisyear()) + '` posts within the `year of ' + str(dt.now().year) + '`')
    writeline(uptime_sheet, '')
    writeline(uptime_sheet, '🦕 there have been `' + str(postcount()) + '` posts `since the dawn of ransomwatch`')
    writeline(uptime_sheet, '')
    writeline(uptime_sheet, '> _the `' + str(version2count()) + '` sites using v2 onion services are no longer indexed - [support.torproject.org](https://support.torproject.org/onionservices/v2-deprecation/)_')
    writeline(uptime_sheet, '')
    writeline(uptime_sheet, '# 📚 index')
    writeline(uptime_sheet, '')
    header = '| group | title | status | last seen | location |'
    writeline(uptime_sheet, header)
    writeline(uptime_sheet, '|---|---|---|---|---|')
    for group in groups:
        stdlog('generating group report for ' + group['name'])
        for host in group['locations']:
            stdlog('generating host report for ' + host['fqdn'])
            if host['available'] is True:
                statusemoji = '⬆️ 🟢'
                lastseen = ''
            elif host['available'] is False:
                # iso timestamp converted to yyyy/mm/dd
                lastseen = host['lastscrape'].split(' ')[0]
                statusemoji = '⬇️ 🔴'
            if host['title'] is not None:
                title = host['title'].replace('|', '-')
            else:
                title = ''
            line = '| ' + group['name'] + ' | ' + title + ' | ' + statusemoji + ' | ' + lastseen + ' | ' + host['fqdn'] + ' |'
            writeline(uptime_sheet, line)

def sidebar():
    '''
    create a sidebar markdown report
    '''
    stdlog('generating sidebar')
    sidebar = 'docs/_sidebar.md'
    # delete contents of file
    with open(sidebar, 'w') as f:
        f.close()
    writeline(sidebar, '- [home](README.md)')
    writeline(sidebar, '- [recent](recentposts.md)')
    writeline(sidebar, '- [stats](stats.md)')
    writeline(sidebar, '- [profiles](profiles.md)')
    stdlog('sidebar generated')

def statspage():
    '''
    create a stats page in markdown containing the plotly graphs
    '''
    stdlog('generating stats page')
    statspage = 'docs/stats.md'
    # delete contents of file
    with open(statspage, 'w') as f:
        f.close()
    writeline(statspage, '# 📊 stats')
    writeline(statspage, '')
    writeline(statspage, ':warning: _data capturing commenced in october 2021 - historic posts may not have accuratley accompanying timestamps before this period_')
    writeline(statspage, '')
    writeline(statspage, '![](postsbygroupmonth.png)')
    writeline(statspage, '')
    writeline(statspage, '![](postsbygroup.png)')
    stdlog('stats page generated')

def recentposts(top):
    '''
    create a list the last X posts (most recent)
    '''
    stdlog('finding recent posts')
    posts = openjson('posts.json')
    # sort the posts by timestamp - descending
    sorted_posts = sorted(posts, key=lambda x: x['discovered'], reverse=True)
    # create a list of the last X posts
    recentposts = []
    for post in sorted_posts:
        recentposts.append(post)
        if len(recentposts) == top:
            break
    stdlog('recent posts generated')
    return recentposts

def recentpage():
    '''create a markdown table for the last 100 posts based on the discovered value'''
    stdlog('generating recent posts page')
    recentpage = 'docs/recentposts.md'
    # delete contents of file
    with open(recentpage, 'w') as f:
        f.close()
    writeline(recentpage, '# 📰 recent posts')
    writeline(recentpage, '')
    writeline(recentpage, '| date | title | group |')
    writeline(recentpage, '|---|---|---|')
    # fetch the 100 most revent posts and add to ascending markdown table
    for post in recentposts(100):
        # show friendly date for discovered
        date = post['discovered'].split(' ')[0]
        # replace markdown tampering characters
        title = post['post_title'].replace('|', '-')
        group = post['group_name'].replace('|', '-')
        grouplink = '[' + group + '](https://ransomwatch.telemetry.ltd/#/profiles?id=' + group + ')'
        line = '| ' + date + ' | `' + title + '` | ' + grouplink + ' |'
        writeline(recentpage, line)
    stdlog('recent posts page generated')

def profilepage():
    '''
    create a profile page for each group in their unique markdown files within docs/profiles
    '''
    stdlog('generating profile pages')
    profilepage = 'docs/profiles.md'
    # delete contents of file
    with open(profilepage, 'w') as f:
        f.close()
    writeline(profilepage, '# 🐦 profiles')
    writeline(profilepage, '')
    emojis = ['🗿','🧱','🧨','💸','🧰','💎','🧲','🧬','🧭','🧮','🧰','🧸','🧻','🧽','❤️‍🔥','💈','🌀','🎟️','🎱','🎲','🐇','🦆','🦈','🦑','👹','🦁','🍟','🍺','🥁','🪂','🗑️','🔋','🔮','🛎️']
    groups = openjson('groups.json')
    for group in groups:
        emoji = emojis[random.randint(0, len(emojis)-1)]
        writeline(profilepage, '## ' + group['name'])
        writeline(profilepage, '')
        if group['captcha'] is True:
            writeline(profilepage, ':warning: _has a captcha_')
            writeline(profilepage, '')
        if group['parser'] is True:
            writeline(profilepage, '_parsing : `enabled`_')
            writeline(profilepage, '')
        else:
            writeline(profilepage, '_parsing : `disabled`_')
            writeline(profilepage, '')
        # add notes if present
        if group['meta'] is not None:
            writeline(profilepage, '_`' + group['meta'] + '`_')
            writeline(profilepage, '')
        if group['javascript_render'] is True:
            writeline(profilepage, '> fetching this site requires a headless browser for javascript processing')
            writeline(profilepage, '')
        if group['geckodriver'] is True:
            writeline(profilepage, '> fetching this site uses geckodriver/selenium')
            writeline(profilepage, '')
        if group['profile'] is not None:
            for profile in group['profile']:
                writeline(profilepage, '- ' + profile)
                writeline(profilepage, '')
        writeline(profilepage, '| title | available | version | last visit | fqdn')
        writeline(profilepage, '|---|---|---|---|---|')        
        for host in group['locations']:
            # convert date to ddmmyyyy hh:mm
            date = host['lastscrape'].split(' ')[0]
            date = date.split('-')
            date = date[2] + '/' + date[1] + '/' + date[0]
            time = host['lastscrape'].split(' ')[1]
            time = time.split(':')
            time = time[0] + ':' + time[1]
            if host['title'] is not None:
                line = '| ' + host['title'] + ' | ' + str(host['available']) +  ' | ' + str(host['version']) + ' | ' + time + ' ' + date + ' | `' + host['fqdn'] + '` |'
                writeline(profilepage, line)
            else:
                line = '| none | ' + str(host['available']) +  ' | ' + str(host['version']) + ' | ' + time + ' ' + date + ' | `' + host['fqdn'] + '` |'
                writeline(profilepage, line)
        writeline(profilepage, '')
        writeline(profilepage, '| post | date |')
        writeline(profilepage, '|---|---|')
        posts = openjson('posts.json')
        for post in posts:
            if post['group_name'] == group['name']:
                date = post['discovered'].split(' ')[0]
                date = date.split('-')
                date = date[2] + '/' + date[1] + '/' + date[0]
                line = '| ' + '`' + post['post_title'].replace('|', '') + '`' + ' | ' + date + ' |'
                writeline(profilepage, line)
        writeline(profilepage, '')
        stdlog('profile page for ' + group['name'] + ' generated')
    stdlog('profile page generation complete')

def main():
    stdlog('generating doco')
    mainpage()
    sidebar()
    recentpage()
    statspage()
    profilepage()
    # if posts.json has been modified within the last 45 mins, assume new posts discovered and recreate graphs
    if os.path.getmtime('posts.json') > (time.time() - (45 * 60)):
        stdlog('posts.json has been modified within the last 45 mins, assuming new posts discovered and recreating graphs')
        groupheatmap()
        barchartgroups()
    else:
        stdlog('posts.json has not been modified within the last 45 mins, assuming no new posts discovered')
