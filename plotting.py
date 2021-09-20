#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import plotly.graph_objects as go

from sharedutils import openjson

def groupreportpie():
    '''
    create a pie to show the number of posts by each group
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
    labels = []
    values = []
    for group in sorted_group_counts:
        labels.append(group[0])
        values.append(group[1])
    fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
    fig.update_layout(title_text='posts by group')
    fig.write_image('docs/postsbygroup.png')

def groupreportmonthly():
    '''chart with plotly the posts by month'''
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
    # create a list of months
    months = []
    for post in posts:
        if post['discovered'].split(' ')[0] not in months:
            months.append(post['discovered'].split(' ')[0])
    # create a list of months with counts
    month_counts = []
    for month in months:
        month_counts.append([month, 0])
    # count the number of posts by group_name within posts.json
    for post in posts:
        for month in month_counts:
            if post['discovered'].split(' ')[0] == month[0]:
                month[1] += 1
    # sort the month_counts - descending
    sorted_month_counts = sorted(month_counts, key=lambda x: x[1], reverse=True)
    # create a list of months
    labels = []
    for month in sorted_month_counts:
        labels.append(month[0])
    # create a list of counts
    values = []
    for month in sorted_month_counts:
        values.append(month[1])
    fig = go.Figure(data=[go.Bar(x=labels, y=values)])
    fig.update_layout(title_text='posts by month')
    fig.write_image('docs/postsbymonth.png')

def groupreportyearly():
    '''
    chart with plotly the posts by year
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
    # create a list of years
    years = []
    for post in posts:
        if post['discovered'].split(' ')[0].split('-')[0] not in years:
            years.append(post['discovered'].split(' ')[0].split('-')[0])
    # create a list of years with counts
    year_counts = []
    for year in years:
        year_counts.append([year, 0])
    # count the number of posts by group_name within posts.json
    for post in posts:
        for year in year_counts:
            if post['discovered'].split(' ')[0].split('-')[0] == year[0]:
                year[1] += 1
    # sort the year_counts - descending
    sorted_year_counts = sorted(year_counts, key=lambda x: x[1], reverse=True)
    # create a list of years
    labels = []
    for year in sorted_year_counts:
        labels.append(year[0])
    # create a list of counts
    values = []
    for year in sorted_year_counts:
        values.append(year[1])
    fig = go.Figure(data=[go.Bar(x=labels, y=values)])
    fig.update_layout(title_text='posts by year')
    fig.write_image('docs/postsbyyear.png')

def uptimechart():
    '''
    graph the uptime of all hosts in groups with plotly
    '''
    groups = openjson('groups.json')
    # count hosts by availability
    up = 0
    down = 0
    for group in groups:
        # count by available key
        for host in group['locations']:
            if host['available'] is True:
                up += 1
            else:
                down += 1
    labels = ['up', 'down']
    values = [up, down]
    fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
    fig.update_layout(title_text='uptime overview')
    fig.write_image('docs/uptime.png')
