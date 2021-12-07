#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt

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

#pie_chart_uptime()
plot_posts_by_group()
