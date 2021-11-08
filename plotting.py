#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import plotly.graph_objects as go

from sharedutils import gcount
from sharedutils import openjson

def groupheatmap():
    '''
    create a heatmap to show the number of posts by group_name within posts.json
    '''
    posts = openjson('posts.json')
    # count the number of posts by group_name within posts.json
    group_counts = gcount(posts)
    # sort the group_counts - descending
    sorted_group_counts = sorted(group_counts.items(), key=lambda x: x[1], reverse=True)
    # create a list of groups
    labels = []
    for group in sorted_group_counts:
        labels.append(group[0])
    # create a list of counts
    values = []
    for group in sorted_group_counts:
        values.append(group[1])
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
    labels2 = []
    for month in sorted_month_counts:
        labels2.append(month[0])
    # create a list of counts
    values2 = []
    for month in sorted_month_counts:
        values2.append(month[1])
    fig = go.Figure(data=[go.Heatmap(x=labels, y=labels2, z=values2)])
    fig.update_layout(title_text='posts by group and month')
    fig.write_image('docs/postsbygroupmonth.png')

def barchartgroups():
    '''
    graph the count of posts by each tracked group
    '''
    posts = openjson('posts.json')
    # count the number of posts by group_name within posts.json
    day_counts = gcount(posts)
    # sort the day_counts - descending
    sorted_day_counts = sorted(day_counts.items(), key=lambda x: x[1], reverse=True)
    # create a list of days
    labels = []
    for day in sorted_day_counts:
        labels.append(day[0])
    # create a list of counts
    values = []
    for day in sorted_day_counts:
        values.append(day[1])
    fig = go.Figure(data=[go.Bar(x=labels, y=values)])
    fig.update_layout(title_text='posts by group')
    fig.write_image('docs/postsbygroup.png')

def scatterplot():
    '''
    create a 3d scatter plot showing the number of posts by group_name within posts.json
    '''
    posts = openjson('posts.json')
    # count the number of posts by group_name within posts.json
    group_counts = gcount(posts)
    # sort the group_counts - descending
    sorted_group_counts = sorted(group_counts.items(), key=lambda x: x[1], reverse=True)
    # create a list of groups
    labels = []
    for group in sorted_group_counts:
        labels.append(group[0])
    # create a list of counts
    values = []
    for group in sorted_group_counts:
        values.append(group[1])
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
    labels2 = []
    for month in sorted_month_counts:
        labels2.append(month[0])
    # create a list of counts
    values2 = []
    for month in sorted_month_counts:
        values2.append(month[1])
    fig = go.Figure(data=[go.Scatter3d(x=labels, y=labels2, z=values2)])
    fig.update_layout(title_text='posts by group and month')
    fig.write_image('docs/3dplot.png')
