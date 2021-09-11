#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
utils to check post titles etc for duplicates or similar posts
'''
import json
import os
import sys
import re
import argparse

# open posts.json from parent directory
with open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'posts.json')) as f:
    posts = json.load(f)
    f.close()

# build a list of all titles
titles = []
for post in posts:
    titles.append(post['post_title'])

# show all titles with a length of 20
for title in titles:
    if len(title) == 20:
        print(title)

exit()

'''
show any exact duplicates
duplicates may not mean parsing issues
at time of writing there are four genuine duplicates
where is appears different groups have made the same posts
'''
for title in titles:
    if titles.count(title) > 1:
        print(title)

'''
show any similar titles
'''
for title in titles:
    if titles.count(title) > 1:
        for title2 in titles:
            if title != title2 and title2.startswith(title):
                print(title2)