#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import datetime
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
    group_counts = [x for x in group_counts if x[0] != 'clop']
    groups = [x[0] for x in group_counts]
    counts = [x[1] for x in group_counts]
    plt.bar(groups, counts, color="#000000")
    plt.title('posts by group')
    plt.xlabel('group name')
    plt.xticks(rotation=90)
    plt.ylabel('# of posts')
    plt.savefig('docs/graphs/postsbygroup.png',dpi=300, bbox_inches="tight", pad_inches=0.1, frameon=False, transparent=True)
    plt.clf()
    plt.cla()

def plot_posts_by_group_past_7_days():
    '''
    plot the number of posts by group over the last week in a barchart
    '''
    posts = openjson('posts.json') 
    seven_days_ago = datetime.datetime.now() - datetime.timedelta(days=7)
    posts = [post for post in posts if post['discovered'] >= seven_days_ago.strftime('%Y-%m-%d')]
    group_counts = gcount(posts)
    group_counts = sorted(group_counts.items(), key=lambda x: x[1], reverse=True)
    group_counts = [x for x in group_counts if x[0] != 'clop']
    groups = [x[0] for x in group_counts]
    counts = [x[1] for x in group_counts]
    plt.bar(groups, counts, color="#000000")
    plt.title('posts by group last 7 days')
    plt.xlabel('group name')
    plt.xticks(rotation=90)
    plt.ylabel('# of posts')
    plt.savefig('docs/graphs/postsbygroup7days.png',dpi=300, bbox_inches="tight", pad_inches=0.1, frameon=False, transparent=True)
    plt.clf()
    plt.cla()

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
    # becomes [{'2021-12-07',4}] etc
    datecount = {}
    for date in dates:
        if date in datecount:
            datecount[date] += 1
        else:
            datecount[date] = 1
    # remove '2021-09-09' - generic date of import along w/ anything before 2021-08
    datecount.pop('2021-09-09', None)
    datecount = {k: v for k, v in datecount.items() if k >= '2021-08-01'}
    datecount = list(datecount.items())
    datecount.sort(key=lambda x: x[0])
    dates = [datetime.datetime.strptime(x[0], '%Y-%m-%d').date() for x in datecount]
    counts = [x[1] for x in datecount]
    plt.plot(dates, counts, color="#000000")
    plt.title('posts per day')
    plt.xlabel('date')
    plt.xticks(rotation=90)
    plt.ylabel('# of posts')
    plt.savefig('docs/graphs/postsbyday.png',dpi=300, bbox_inches="tight", pad_inches=0.1, frameon=False, transparent=True)
    plt.clf()
    plt.cla()

def pie_posts_by_group():
    '''
    plot the number of posts by group in a pie
    '''
    posts = openjson('posts.json')
    group_counts = gcount(posts)
    group_counts = sorted(group_counts.items(), key=lambda x: x[1], reverse=True)
    group_counts = [x for x in group_counts if x[0] != 'clop']
    groups = [x[0] for x in group_counts]
    counts = [x[1] for x in group_counts]
    # ignoring the top 10 groups, merge the rest into "other"
    topgroups = groups[:10]
    topcounts = counts[:10]
    othercounts = counts[10:]
    othercount = sum(othercounts)
    topgroups.append('other')
    topcounts.append(othercount)
    colours = ['#ffc09f','#ffee93','#fcf5c7','#a0ced9','#adf7b6','#e8dff5','#fce1e4','#fcf4dd','#ddedea','#daeaf6','#79addc','#ffc09f','#ffee93','#fcf5c7','#adf7b6']
    plt.pie(topcounts, labels=topgroups, autopct='%1.1f%%', startangle=140, labeldistance=1.1, pctdistance=0.8, colors=colours)
    plt.legend(loc='lower center', bbox_to_anchor=(0.5, -0.2), ncol=3)
    plt.text(0.5, 0.5, 'total : ' + str(sum(counts)), horizontalalignment='center', verticalalignment='center', transform=plt.gcf().transFigure)
    plt.title('posts by group')
    plt.savefig('docs/graphs/grouppie.png',dpi=300, bbox_inches="tight", pad_inches=0.1, frameon=False, transparent=True)
    plt.clf()
    plt.cla()
