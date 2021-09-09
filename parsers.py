#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
parses the source html for each group where a parser exists & contributed to the post dictionary
always remember..... https://stackoverflow.com/questions/1732348/regex-match-open-tags-except-xhtml-self-contained-tags/1732454#1732454
'''
import json
from datetime import datetime

from sharedutils import openjson
from sharedutils import runshellcmd

from sharedutils import stdlog, dbglog, errlog, honk

def posttemplate(victim, group_name, timestamp):
    '''
    assuming we have a new post - form the template we will use for the new entry in posts.json
    '''
    schema = {
        'post_title': victim,
        'group_name': group_name,
        'discovered': timestamp
    }
    stdlog('new post: ' + victim)
    dbglog(schema)
    return schema

def ispostnew(post_title, group_name):
    '''
    check if a post already exists in posts.json
    '''
    posts = openjson('posts.json')
    for post in posts:
        dbglog('checking post: ' + post['post_title'])
        if post['post_title'] == post_title and post['group_name'] == group_name:
            stdlog('post already exists: ' + post_title)
            return True
    stdlog('post does not exist: ' + post_title)
    return False

def appender(post_title, group_name):
    '''
    append a new post to posts.json
    '''
    if ispostnew(post_title, group_name):
        posts = openjson('posts.json')
        newpost = posttemplate(post_title, group_name, str(datetime.today()))
        stdlog('adding new post: ' + 'group:' + group_name + 'title:' + post_title)
        posts.append(newpost)
        with open('posts.json', 'w') as outfile:
            '''
            use ensure_ascii to mandate utf-8 in the case the post contains cyrillic 🇷🇺
            https://pynative.com/python-json-encode-unicode-and-non-ascii-characters-as-is/
            '''
            dbglog('writing changes to posts.json')
            json.dump(posts, outfile, indent=4, ensure_ascii=False)

'''
all parsers here are shell - mix of grep/sed/awk & perl - runshellcmd is a wrapper for subprocess.run
'''

def synack():
    stdlog('parser: ' + 'synack')
    parser='''
    grep 'card-title' source/synack*.html --no-filename | cut -d ">" -f2 | cut -d "<" -f1
    '''
    posts = runshellcmd(parser)
    for post in posts:
        appender(post, 'synack')

def suncrypt():
    stdlog('parser: ' + 'suncrypt')
    parser = '''
    cat source/suncrypt-*.html | tr '>' '\n' | grep -A1 '<a href="client?id=' | sed '/^--/d' | sed '/^<a/d' | cut -d '<' -f1 | sed 's/[ \t]*$//' "$@"
    '''
    posts = runshellcmd(parser)
    for post in posts:
        appender(post, 'suncrypt')

def lorenz():
    stdlog('parser: ' + 'lorenz')
    parser = '''
    grep 'h3' source/lorenz*.html --no-filename | cut -d ">" -f2 | cut -d "<" -f1 | sed -e 's/^ *//g' -e '/^$/d'
    '''
    posts = runshellcmd(parser)
    for post in posts:
        appender(post, 'lorenz')

def lockbit2():
    stdlog('parser: ' + 'lockbit2')
    parser = '''
    awk '/<div class=post-title>/{getline; print}' source/lockbit2*.html | cut -d '<' -f1
    '''
    posts = runshellcmd(parser)
    for post in posts:
        appender(post, 'lockbit2')

'''
used to fetch the description of a lb2 post - not used
'''    
# def lockbit2desc():
#     stdlog('parser: ' + 'lockbit2desc')
#     parser = '''
#     sed -n '/post-block-text/{n;p;}' source/lockbit2*.html | sed '/^</d' | cut -d "<" -f1
#     '''
#     posts = runshellcmd(parser)
#     for post in posts:
#         appender(post, 'lockbit2')

def arvinclub():
    stdlog('parser: ' + 'arvinclub')
    parser = '''
    grep 'bookmark' source/arvinclub*.html --no-filename | cut -d ">" -f3 | cut -d "<" -f1
    '''
    posts = runshellcmd(parser)
    for post in posts:
        appender(post, 'arvinclub')

def avoslocker():
    stdlog('parser: ' + 'avoslocker')
    parser = '''
    sed -n -e 's/^.*aria-hidden="true"><\/i> //p' source/avoslocker-*.html | cut -d "<" -f1
    '''
    posts = runshellcmd(parser)
    for post in posts:
        appender(post, 'avoslocker')

def avaddon():
    stdlog('parser: ' + 'avaddon')
    parser = '''
    grep 'h6' source/avaddon*.html --no-filename | cut -d ">" -f3 | sed -e s/'<\/a'// | tee -a normalised/avaddon.txt
    '''
    posts = runshellcmd(parser)
    for post in posts:
        appender(post, 'avaddon')

def xinglocker():
    stdlog('parser: ' + 'xinglocker')
    parser = '''
    grep "h3" -A1 source/xinglocker*.html --no-filename | grep -v h3 | awk -v n=4 'NR%n==1' | sed -e 's/^[ \t]*//'
    '''
    posts = runshellcmd(parser)
    for post in posts:
        appender(post, 'xinglocker')
    
def ragnarlocker():
    stdlog('parser: ' + 'ragnarlocker')
    json_parser = '''
    grep 'var post_links' source/ragnarlocker*.html --no-filename | sed -e s/"        var post_links = "// -e "s/ ;//"
    '''
    posts = runshellcmd(json_parser)
    post_json = json.loads(posts[0])
    for post in post_json:
        appender(post['title'], 'ragnarlocker')

def clop():
    stdlog('parser: ' + 'clop')
    parser = '''
    grep 'PUBLISHED' source/clop*.html --no-filename | sed -e s/"<strong>"// -e s/"<\/strong>"// -e s/"<\/p>"// -e s/"<p>"// -e s/"<br>"// -e s/"<strong>"// -e s/"<\/strong>"//
    '''
    posts = runshellcmd(parser)
    for post in posts:
        appender(post, 'clop')

def revil():
    stdlog('parser: ' + 'revil')
    parser = '''
    grep 'href="/posts' source/revil*.html --no-filename | cut -d '>' -f2 | sed -e s/'<\/a'// -e 's/^[ \t]*//'
    '''
    posts = runshellcmd(parser)
    for post in posts:
        appender(post, 'revil')

def ragnarok():
    stdlog('parser: ' + 'ragnarok')
    parser = '''
    grep '<h2 class="title">' -A2 source/ragnarok-*.html --no-filename | grep -wv 'h2 class\|href' | sed '/^--/d' | sed 's/^ *//g'
    '''
    posts = runshellcmd(parser)
    for post in posts:
        appender(post, 'ragnarok')

def conti():
    stdlog('parser: ' + 'conti')
    parser = '''
    grep 'class="title">&' source/conti*.html --no-filename | cut -d ";" -f2 | sed -e s/"&rdquo"//
    '''
    posts = runshellcmd(parser)
    for post in posts:
        appender(post, 'conti')
    
def pysa():
    stdlog('parser: ' + 'pysa')
    parser = '''
    grep 'icon-chevron-right' source/pysa*.html --no-filename | cut -d '>' -f3 | sed 's/^ *//g'
    '''
    posts = runshellcmd(parser)
    for post in posts:
        appender(post, 'pysa')

def nefilim():
    stdlog('parser: ' + 'nefilim')
    parser = '''
    grep 'h2' source/nefilim*.html --no-filename | cut -d '>' -f3 | sed -e s/'<\/a'//
    '''
    posts = runshellcmd(parser)
    for post in posts:
        appender(post, 'nefilim') 

def mountlocker():
    stdlog('parser: ' + 'mountlocker')
    parser = '''
    grep '<h3><a href=' source/mount-locker*.html --no-filename | cut -d '>' -f5 | sed -e s/'<\/a'// | sed 's/^ *//g'
    '''
    posts = runshellcmd(parser)
    for post in posts:
        appender(post, 'mountlocker')

def babuklocker():
    stdlog('parser: ' + 'babuklocker')
    parser = '''
    grep '<h5>' source/babuk-locker-*.html --no-filename | sed 's/^ *//g' | cut -d '>' -f2 | cut -d '<' -f1 | grep -wv 'Hospitals\|Non-Profit\|Schools\|Small Business' | sed '/^[[:space:]]*$/d'
    '''
    posts = runshellcmd(parser)
    for post in posts:
        appender(post, 'babuklocker')
    
def ransomexx():
    stdlog('parser: ' + 'ransomexx')
    parser = '''
    grep 'card-title' source/ransomexx*.html --no-filename | cut -d '>' -f2 | sed -e s/'<\/h5'//
    '''
    posts = runshellcmd(parser)
    for post in posts:
        appender(post, 'ransomexx')

def cuba():
    stdlog('parser: ' + 'cuba')
    parser = '''
    grep '<p>' source/cuba*.html --no-filename | cut -d '>' -f3 | cut -d '<' -f1
    '''
    posts = runshellcmd(parser)
    for post in posts:
        appender(post, 'cuba')

def pay2key():
    stdlog('parser: ' + 'pay2key')
    parser = '''
    grep 'h3><a href' source/pay2key*.html --no-filename | cut -d '>' -f3 | sed -e s/'<\/a'//
    '''
    posts = runshellcmd(parser)
    for post in posts:
        appender(post, 'pay2key')

def azroteam():
    stdlog('parser: ' + 'azroteam')
    parser = '''
    grep "h3" -A1 source/aztroteam*.html --no-filename | grep -v h3 | awk -v n=4 'NR%n==1' | sed -e 's/^[ \t]*//'
    '''
    posts = runshellcmd(parser)
    for post in posts:
        appender(post, 'azroteam')

def lockdata():
    stdlog('parser: ' + 'lockdata')
    parser = '''
    grep '<a href="/view.php?' source/lockdata-*.html --no-filename | cut -d '>' -f2 | cut -d '<' -f1
    '''
    posts = runshellcmd(parser)
    for post in posts:
        appender(post, 'lockdata')
    
def blacktor():
    stdlog('parser: ' + 'blacktor')
    parser = '''
    sed -n '/tr/{n;p;}' source/bl@cktor-*.html | grep 'td' | cut -d '>' -f2 | cut -d '<' -f1
    '''
    posts = runshellcmd(parser)
    for post in posts:
        appender(post, 'blacktor')
    
def darkleakmarket():
    stdlog('parser: ' + 'darkleakmarket')
    parser = '''
    grep 'page.php' source/darkleakmarket-*.html --no-filename | sed -e 's/^[ \t]*//' | cut -d '>' -f3 | sed '/^</d' | cut -d '<' -f1
    '''
    posts = runshellcmd(parser)
    for post in posts:
        appender(post, 'darkleakmarket')

def blackmatter():
    stdlog('parser: ' + 'blackmatter')
    parser = '''
    grep '<h4>' source/blackmatter-* --no-filename |  sed 's/^ *//g' | cut -d '>' -f2 | cut -d '<' -f1
    '''
    posts = runshellcmd(parser)
    for post in posts:
        appender(post, 'blackmatter')

def payloadbin():
    stdlog('parser: ' + 'payloadbin')
    parser = '''
    grep '<h4 class="h4' source/payloadbin-* --no-filename | cut -d '>' -f3 | cut -d '<' -f 1
    '''
    posts = runshellcmd(parser)
    for post in posts:
        appender(post, 'payloadbin')

def groove():
    stdlog('parser: ' + 'groove')
    parser = '''
    egrep -o 'class="title">([[:alnum:]]| |\.)+</a>' source/groove-* | cut -d '>' -f2 | cut -d '<' -f 1
    '''
    posts = runshellcmd(parser)
    for post in posts:
        appender(post, 'groove')
