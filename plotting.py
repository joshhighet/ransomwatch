#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt

from sharedutils import gcount
from sharedutils import openjson

'''
the date field in posts is 'discovered' - YYYY-MM-DD HH:MM:SS.SSSSSS
gcount returns a list i.e {'suncrypt': 15, 'lorenz': 18, 'arvinclub': 15}
'''

def plot_posts_by_group():
    # open up the posts dictionary
    posts = openjson('posts.json')
    # create a list of groups and their count
    group_counts = gcount(posts)
    # we want to sort this list by the count
    group_counts = sorted(group_counts.items(), key=lambda x: x[1], reverse=True)
    # create a list of the groups
    groups = [x[0] for x in group_counts]
    # create a list of the counts
    counts = [x[1] for x in group_counts]
    # create a bar chart
    plt.bar(groups, counts)
    # set the title
    plt.title('posts by group')
    # set the x-axis label - the names are long so horizontal labels are better
    plt.xlabel('group name')
    plt.xticks(rotation=90)
    # set the y-axis label
    plt.ylabel('# of posts')
    # save the plot to a file
    plt.savefig('docs/graphs/posts_by_group.png',dpi=300, bbox_inches = "tight")

plot_posts_by_group()