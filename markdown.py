#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import random
from datetime import datetime as dt

from sharedutils import openjson
from sharedutils import postcount
from sharedutils import groupcount
from sharedutils import parsercount
from sharedutils import hostcount
from sharedutils import headlesscount
from sharedutils import onlinecount
from sharedutils import version2count
from sharedutils import mounthlypostcount
from sharedutils import postssince
from sharedutils import poststhisyear
from sharedutils import postslast24h
from sharedutils import currentmonthstr
from sharedutils import countcaptchahosts
from sharedutils import groupreportyearly
from sharedutils import groupreportmonthly
from sharedutils import groupreportpie
from sharedutils import uptimechart

def suffix(d):
    return 'th' if 11<=d<=13 else {1:'st',2:'nd',3:'rd'}.get(d%10, 'th')

def custom_strftime(format, t):
    return t.strftime(format).replace('{S}', str(t.day) + suffix(t.day))

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
    return sorted_group_counts

def mainpage():
    '''
    main markdown report generator - used with github pages
    '''
    uptime_sheet = 'docs/README.md'
    with open(uptime_sheet, 'w') as f:
        f.close()
    groups = openjson('groups.json')
    writeline(uptime_sheet, '## 📰 summary - ' + friendly_tz)
    writeline(uptime_sheet, '')
    writeline(uptime_sheet, 'currently tracking `' + str(groupcount()) + '` groups across `' + str(hostcount()) + '` various relays and mirrors - ' + '_`' + str(onlinecount()) + '` of which are online_')
    writeline(uptime_sheet, '')
    writeline(uptime_sheet, 'there are currently `' + str(parsercount()) + '` active parsers, `' + str(headlesscount()) + '` of which requiring headless browsers - _`' + str(countcaptchahosts()) + '` groups have introduced captchas this year_')
    writeline(uptime_sheet, '')
    writeline(uptime_sheet, '⏲ there have been `' + str(postslast24h()) + '` posts within the `last 24 hours`')
    writeline(uptime_sheet, '')
    writeline(uptime_sheet, '🦈 there have been `' + str(mounthlypostcount()) + '` posts within the `month of ' + currentmonthstr() + '`')
    writeline(uptime_sheet, '')
    writeline(uptime_sheet, '🪐 there have been `' + str(postssince(90)) + '` posts within the `last 90 days`')
    writeline(uptime_sheet, '')
    writeline(uptime_sheet, '🏚 there have been `' + str(poststhisyear()) + '` posts within the `year of ' + str(dt.now().year) + '`')
    writeline(uptime_sheet, '')
    writeline(uptime_sheet, '🦕 there have been `' + str(postcount()) + '` posts `since the beginning of time`')
    writeline(uptime_sheet, '')
    writeline(uptime_sheet, '> _the `' + str(version2count()) + '` sites using v2 onion services are no longer indexed - [support.torproject.org](https://support.torproject.org/onionservices/v2-deprecation/)_')
    writeline(uptime_sheet, '')
    writeline(uptime_sheet, '# 📚 index')
    writeline(uptime_sheet, '')
    header = '| group | title | status | last seen | location |'
    writeline(uptime_sheet, header)
    writeline(uptime_sheet, '|---|---|---|---|---|')
    for group in groups:
        for host in group['locations']:
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
    sidebar = 'docs/_sidebar.md'
    # delete contents of file
    with open(sidebar, 'w') as f:
        f.close()
    writeline(sidebar, '- [home](README.md)')
    writeline(sidebar, '- [recent](recentposts.md)')
    writeline(sidebar, '- [stats](stats.md)')
    writeline(sidebar, '- [profiles](profiles.md)')
    groups = openjson('groups.json')

def statspage():
    '''
    create a stats page in markdown containing the plotly graphs
    '''
    statspage = 'docs/stats.md'
    # delete contents of file
    with open(statspage, 'w') as f:
        f.close()
    writeline(statspage, '# 📊 stats')
    writeline(statspage, '')
    writeline(statspage, '![](postsbygroup.png)')
    writeline(statspage, '')
    writeline(statspage, '![](uptime.png)')
    writeline(statspage, '')
    writeline(statspage, ':warning: _data capturing commenced in october 2021 - historic posts may not have accuratley accompanying timestamps before this period_')
    writeline(statspage, '')
    writeline(statspage, '![](postsbymonth.png)')
    writeline(statspage, '')
    writeline(statspage, '![](postsbyyear.png)')

def recentposts(top):
    '''
    create a list the last X posts (most recent)
    '''
    posts = openjson('posts.json')
    # sort the posts by timestamp - descending
    sorted_posts = sorted(posts, key=lambda x: x['discovered'], reverse=True)
    # create a list of the last X posts
    recentposts = []
    for post in sorted_posts:
        recentposts.append(post)
        if len(recentposts) == top:
            break
    return recentposts

def recentpage():
    '''create a markdown table for the last 30 posts based on the discovered value'''
    recentpage = 'docs/recentposts.md'
    # delete contents of file
    with open(recentpage, 'w') as f:
        f.close()
    writeline(recentpage, '# 📰 recent posts')
    writeline(recentpage, '')
    writeline(recentpage, '| date | title | group |')
    writeline(recentpage, '|---|---|---|')
    # fetch the 30 most revent posts and add to ascending markdown table
    for post in recentposts(30):
        # show friendly date for discovered
        date = post['discovered'].split(' ')[0]
        # replace markdown tampering characters
        title = post['post_title'].replace('|', '-')
        group = post['group_name'].replace('|', '-')
        line = '| ' + date + ' | `' + title + '` | ' + group + ' |'
        writeline(recentpage, line)

def profilepage():
    '''
    create a profile page for each group in their unique markdown files within docs/profiles
    '''
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
        writeline(profilepage, '## ' + emoji + ' ' + group['name'])
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
            writeline(profilepage, '`' + group['meta'] + '`_')
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
                line = '| ' + '`' + post['post_title'] + '`' + ' | ' + date + ' |'
                writeline(profilepage, line)


def main():
    mainpage()
    sidebar()
    recentpage()
    groupreportyearly()
    groupreportmonthly()
    groupreportpie()
    uptimechart()
    statspage()
    profilepage()