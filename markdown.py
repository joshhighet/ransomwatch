#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime as dt

from sharedutils import openjson
from sharedutils import postcount
from sharedutils import groupcount
from sharedutils import parsercount
from sharedutils import hostcount
from sharedutils import geckocount
from sharedutils import onlinecount
from sharedutils import version2count
from sharedutils import mounthlypostcount
from sharedutils import postssince
from sharedutils import poststhisyear
from sharedutils import postslast24h
from sharedutils import currentmonthstr
from sharedutils import offlinegroups24h
from sharedutils import countcaptchahosts
from sharedutils import groupreportyearly
from sharedutils import groupreportmonthly
from sharedutils import groupreportpie

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
    create a figure on the number of posts by respective group
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
    # delete contents of file
    with open(uptime_sheet, 'w') as f:
        f.close()
    groups = openjson('groups.json')
    # start markdown formatting
    # writeline(uptime_sheet, '# [ransomwatch](https://github.com/thetanz/ransomwatch)')
    # writeline(uptime_sheet, '')
    writeline(uptime_sheet, '## 📰 summary - ' + friendly_tz)
    writeline(uptime_sheet, '')
    writeline(uptime_sheet, 'currently tracking `' + str(groupcount()) + '` groups across `' + str(hostcount()) + '` various relays and mirrors - ' + '_`' + str(onlinecount()) + '` of which are online, with `' + str(geckocount()) + '` appearing inaccessible_')
    writeline(uptime_sheet, '')
    writeline(uptime_sheet, 'there are currently `' + str(parsercount()) + '` active parsers, `' + str(geckocount()) + '` of which leverage [mozilla/geckodriver](https://github.com/mozilla/geckodriver) - _`' + str(countcaptchahosts()) + '` groups have introduced captchas this year_')
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
    #offlinepast24h = offlinegroups24h()
    #writeline(uptime_sheet, '`' + str(len(offlinepast24h)) + '` locations have gone offline within the past 24 hours')
    #writeline(uptime_sheet, '')
    #for offlinehost in offlinepast24h:
    #    writeline(uptime_sheet, '- ' + offlinehost)
    #writeline(uptime_sheet, '')
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
    writeline(sidebar, '- [stats](stats.md)')
    writeline(sidebar, '- [profiles](profiles.md)')
    #writeline(sidebar, '    - [stats](stats.md)')
    #writeline(sidebar, '    - [recent](recentposts.md)')
    # writeline(sidebar, '- groups')
    # '''create a de-duplicated list of groups'''
    # group_list = []
    # groups = openjson('groups.json')
    # for group in groups:
    #     if group['name'] not in group_list:
    #         group_list.append(group['name'])
    # for uniqgroup in group_list:
    #     line = '    - ' + '[' + uniqgroup + '](' + uniqgroup + '.md)'
    #     writeline(sidebar, line)

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
    writeline(statspage, ':warning: _data capturing commenced in september 2021 - historic posts may not have accuratley accompanying timestamps before this period_')
    writeline(statspage, '')
    writeline(statspage, '![](postsbymonth.png)')
    writeline(statspage, '')
    writeline(statspage, '![](postsbyyear.png)')

def recentposts():
    produce = 30
    '''create a markdown table for the <produce> most recent posts based on the discovered field in posts.json'''
    recentposts = 'docs/recentposts.md'
    # delete contents of file
    with open(recentposts, 'w') as f:
        f.close()
    writeline(recentposts, '# 📰 recent posts')
    writeline(recentposts, '')
    writeline(recentposts, '_`' + str(produce) + '`' + ' most recent posts_')
    writeline(recentposts, '')
    writeline(recentposts, '| date | title | group |')
    writeline(recentposts, '|---|---|---|')
    posts = openjson('posts.json')
    for post in posts[-produce:]:
        # convert long date to ddmmyyyy
        date = post['discovered'].split(' ')[0]
        date = date.split('-')
        date = date[2] + '/' + date[1] + '/' + date[0]
        line = '| ' + date + ' | ' + '`' + post['post_title'] + '`' + ' | ' + post['group_name'] + ' |'
        writeline(recentposts, line)

def main():
    mainpage()
    sidebar()
    # recentposts()
    groupreportyearly()
    groupreportmonthly()
    groupreportpie()
    statspage()

def profilepage():
    '''
    create a profile page in markdown containing the plotly graphs
    '''
    profilepage = 'docs/profiles.md'
    # delete contents of file
    with open(profilepage, 'w') as f:
        f.close()
    writeline(profilepage, '# 📚 profiles')
    writeline(profilepage, '')
    groups = openjson('groups.json')
    for group in groups:
        writeline(profilepage, '## ' + group['name'])
        writeline(profilepage, '')
        # if group meta is not none, write it
        if group['meta'] is not None:
            writeline(profilepage, '_notes: `' + group['meta'] + '`_')
            writeline(profilepage, '')
        if group['profile'] is not None:
            for profile in group['profile']:
                writeline(profilepage, '- ' + profile)
                writeline(profilepage, '')

profilepage()