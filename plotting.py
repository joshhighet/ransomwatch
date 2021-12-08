#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from sharedutils import gcount
from sharedutils import openjson

def plot_posts_by_group():
    '''
    plot the number of posts by group in a barchart
    '''
    posts = openjson('posts.json') 
    group_counts = gcount(posts)
    group_counts = sorted(group_counts.items(), key=lambda x: x[1], reverse=True)
    groups = [x[0] for x in group_counts]
    counts = [x[1] for x in group_counts]
    plt.bar(groups, counts)
    plt.title('posts by group')
    plt.xlabel('group name')
    plt.xticks(rotation=90)
    plt.ylabel('# of posts')
    plt.savefig('docs/graphs/posts_by_group.png',dpi=300, bbox_inches="tight")

def pie_chart_uptime():
    '''
    plot the uptime of the bot in a pie chart
    '''
    groups = openjson('groups.json')
    available = 0
    unavailable = 0
    for group in groups:
        for host in group['locations']:
            if host['available'] == True:
                available += 1
            elif host['available'] == False:
                unavailable += 1
    labels = ['up', 'down']
    sizes = [available, unavailable]
    colors = ['green', 'red']
    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')
    plt.title('group monitoring availability')
    plt.savefig('docs/graphs/uptime.png',dpi=300, bbox_inches="tight")

def trend_posts_per_day():
    '''
    plot the trend of the number of posts per day
    '''
    posts = openjson('posts.json')
    dates = []
    for post in posts:
        dates.append(post['discovered'][0:10])
    # list of duplicate dates should be marged to show a count of posts per day
    # i.e ['2021-12-07', '2021-12-07', '2021-12-07', '2021-12-07', '2021-12-07']
    # becomes [{'2021-12-07',4}]
    datecount = {}
    for date in dates:
        if date in datecount:
            datecount[date] += 1
        else:
            datecount[date] = 1
    # remove '2021-09-09' - generic date of import
    datecount.pop('2021-09-09', None)
    # remove anything before 2021-08
    datecount = {k: v for k, v in datecount.items() if k >= '2021-08-01'}
    # now we have a dictionary of dates and counts - {'2021-08-10': 1, '2021-07-29': 1, '2021-07-27': 3}
    # convert to list of tuples
    datecount = list(datecount.items())
    # sort by date
    datecount.sort(key=lambda x: x[0])
    # dates should be in datetime format so formatted correctly in matplotlib output
    dates = [datetime.datetime.strptime(x[0], '%Y-%m-%d').date() for x in datecount]
    counts = [x[1] for x in datecount]
    plt.plot(dates, counts)
    plt.title('posts per day')
    plt.xlabel('date')
    plt.xticks(rotation=90)
    plt.ylabel('# of posts')
    plt.savefig('docs/graphs/posts_per_day.png',dpi=300, bbox_inches="tight")

def stackplot_posts_by_group_by_day():
    '''
    plot the number of posts by group in a stacked bar chart
    each group should be a different color and each day should be a different bar
    '''
    posts = openjson('posts.json')
    group_counts = {}
    for post in posts:
        if post['group_name'] in group_counts:
            if post['discovered'][0:10] in group_counts[post['group_name']]:
                group_counts[post['group_name']][post['discovered'][0:10]] += 1
            else:
                group_counts[post['group_name']][post['discovered'][0:10]] = 1
        else:
            group_counts[post['group_name']] = {}
            group_counts[post['group_name']][post['discovered'][0:10]] = 1
    group_counts = list(group_counts.items())
    group_counts.sort(key=lambda x: x[0])
    # [('midas', {'2021-11-29': 25}), ('robinhood', {'2021-12-06': 1}), ('snatch', {'2021-11-29': 10, '2021-11-30': 2, '2021-12-02': 2})]
    print(group_counts)
    
#trend_posts_per_day()
#pie_chart_uptime()
#plot_posts_by_group()
#stackplot_posts_by_group_by_day()