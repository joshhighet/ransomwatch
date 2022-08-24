#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
parses the source html for each group where a parser exists & contributed to the post dictionary
always remember..... https://stackoverflow.com/questions/1732348/regex-match-open-tags-except-xhtml-self-contained-tags/1732454#1732454
'''
import os
import json
from sys import platform
from datetime import datetime

from sharedutils import openjson
from sharedutils import runshellcmd
from sharedutils import todiscord, totwitter, toteams
from sharedutils import stdlog, dbglog, errlog, honk

# on macOS we use 'grep -oE' over 'grep -oP'
if platform == 'darwin':
    fancygrep = 'grep -oE'
else:
    fancygrep = 'grep -oP'

def posttemplate(victim, group_name, timestamp):
    '''
    assuming we have a new post - form the template we will use for the new entry in posts.json
    '''
    schema = {
        'post_title': victim,
        'group_name': group_name,
        'discovered': timestamp
    }
    dbglog(schema)
    return schema

def existingpost(post_title, group_name):
    '''
    check if a post already exists in posts.json
    '''
    posts = openjson('posts.json')
    # posts = openjson('posts.json')
    for post in posts:
        if post['post_title'] == post_title and post['group_name'] == group_name:
            #dbglog('post already exists: ' + post_title)
            return True
    dbglog('post does not exist: ' + post_title)
    return False

def appender(post_title, group_name):
    '''
    append a new post to posts.json
    '''
    if len(post_title) == 0:
        errlog('post_title is empty')
        return
    # limit length of post_title to 90 chars
    if len(post_title) > 90:
        post_title = post_title[:90]
    if existingpost(post_title, group_name) is False:
        posts = openjson('posts.json')
        newpost = posttemplate(post_title, group_name, str(datetime.today()))
        stdlog('adding new post - ' + 'group:' + group_name + ' title:' + post_title)
        posts.append(newpost)
        with open('posts.json', 'w', encoding='utf-8') as outfile:
            '''
            use ensure_ascii to mandate utf-8 in the case the post contains cyrillic 🇷🇺
            https://pynative.com/python-json-encode-unicode-and-non-ascii-characters-as-is/
            '''
            dbglog('writing changes to posts.json')
            json.dump(posts, outfile, indent=4, ensure_ascii=False)
        # if socials are set try post
        if os.environ.get('DISCORD_WEBHOOK') is not None:
            todiscord(newpost['post_title'], newpost['group_name'])
        if os.environ.get('TWITTER_ACCESS_TOKEN') is not None:
            totwitter(newpost['post_title'], newpost['group_name'])
        if os.environ.get('MS_TEAMS_WEBHOOK') is not None:
            toteams(newpost['post_title'], newpost['group_name'])

'''
all parsers here are shell - mix of grep/sed/awk & perl - runshellcmd is a wrapper for subprocess.run
'''

def synack():
    stdlog('parser: ' + 'synack')
    parser='''
    grep 'card-title' source/synack-*.html --no-filename | cut -d ">" -f2 | cut -d "<" -f1
    '''
    posts = runshellcmd(parser)
    if len(posts) == 1:
        errlog('synack: ' + 'parsing fail')
    for post in posts:
        appender(post, 'synack')

def everest():
    stdlog('parser: ' + 'everest')
    parser = '''
    grep '<h2 class="entry-title' source/everest-*.html | cut -d '>' -f3 | cut -d '<' -f1
    '''
    posts = runshellcmd(parser)
    if len(posts) == 1:
        errlog('everest: ' + 'parsing fail')
    for post in posts:
        appender(post, 'everest')


def suncrypt():
    stdlog('parser: ' + 'suncrypt')
    parser = '''
    cat source/suncrypt-*.html | tr '>' '\n' | grep -A1 '<a href="client?id=' | sed -e '/^--/d' -e '/^<a/d' | cut -d '<' -f1 | sed -e 's/[ \t]*$//' "$@" -e '/Read more/d'
    '''
    posts = runshellcmd(parser)
    if len(posts) == 1:
        errlog('suncrypt: ' + 'parsing fail')
    for post in posts:
        appender(post, 'suncrypt')

def lorenz():
    stdlog('parser: ' + 'lorenz')
    parser = '''
    grep 'h3' source/lorenz-*.html --no-filename | cut -d ">" -f2 | cut -d "<" -f1 | sed -e 's/^ *//g' -e '/^$/d' -e 's/[[:space:]]*$//'
    '''
    posts = runshellcmd(parser)
    if len(posts) == 1:
        errlog('lorenz: ' + 'parsing fail')
    for post in posts:
        appender(post, 'lorenz')

def lockbit2():
    stdlog('parser: ' + 'lockbit2')
    # egrep -h -A1 'class="post-title"' source/lockbit2-* | grep -v 'class="post-title"' | grep -v '\--' | cut -d'<' -f1 | tr -d ' '
    parser = '''
    awk -v lines=2 '/post-title-block/ {for(i=lines;i;--i)getline; print $0 }' source/lockbit2-*.html | cut -d '<' -f1 | sed -e 's/^ *//g' -e 's/[[:space:]]*$//' | sort | uniq
    '''
    posts = runshellcmd(parser)
    if len(posts) == 1:
        errlog('lockbit2: ' + 'parsing fail')
    for post in posts:
        appender(post, 'lockbit2')

'''
used to fetch the description of a lb2 post - not used
def lockbit2desc():
    stdlog('parser: ' + 'lockbit2desc')
    # sed -n '/post-block-text/{n;p;}' source/lockbit2-*.html | sed '/^</d' | cut -d "<" -f1
    posts = runshellcmd(parser)
    if len(posts) == 1:
        errlog('lockbit2: ' + 'parsing fail')
    for post in posts:
        appender(post, 'lockbit2')
'''

def arvinclub():
    stdlog('parser: ' + 'arvinclub')
    # grep 'bookmark' source/arvinclub-*.html --no-filename | cut -d ">" -f3 | cut -d "<" -f1
    parser = '''
    grep 'rel="bookmark">' source/arvinclub-*.html -C 1 | grep '</a>' | sed 's/^[^[:alnum:]]*//' | cut -d '<' -f 1 | sed -e 's/^ *//g' -e 's/[[:space:]]*$//'
    '''
    posts = runshellcmd(parser)
    if len(posts) == 1:
        errlog('arvinclub: ' + 'parsing fail')
    for post in posts:
        appender(post, 'arvinclub')

def hiveleak():
    stdlog('parser: ' + 'hiveleak')
    # grep 'bookmark' source/hive-*.html --no-filename | cut -d ">" -f3 | cut -d "<" -f1
    # egrep -o 'class="">([[:alnum:]]| |\.)+</h2>' source/hiveleak-hiveleak*.html | cut -d '>' -f 2 | cut -d '<' -f 1 && egrep -o 'class="lines">([[:alnum:]]| |\.)+</h2>' source/hiveleak-hiveleak*.html | cut -d '>' -f 2 | cut -d '<' -f 1 | sort -u
    # egrep -o 'class="lines">.*?</h2>' source/hiveleak-hiveleak*.html | cut -d '>' -f 2 | cut -d '<' -f 1 && egrep -o 'class="lines">.*?</h2>' source/hiveleak-hiveleak*.html | cut -d '>' -f 2 | cut -d '<' -f 1 | sort -u
    parser = '''
    jq -r '.[].title' source/hiveleak-hiveapi*.html || true
    '''
    posts = runshellcmd(parser)
    if len(posts) == 1:
        errlog('hiveleak: ' + 'parsing fail')
    for post in posts:
        appender(post, 'hiveleak')

def avaddon():
    stdlog('parser: ' + 'avaddon')
    parser = '''
    grep 'h6' source/avaddon-*.html --no-filename | cut -d ">" -f3 | sed -e s/'<\/a'//
    '''
    posts = runshellcmd(parser)
    if len(posts) == 1:
        errlog('avaddon: ' + 'parsing fail')
    for post in posts:
        appender(post, 'avaddon')

def xinglocker():
    stdlog('parser: ' + 'xinglocker')
    parser = '''
    grep "h3" -A1 source/xinglocker-*.html --no-filename | grep -v h3 | awk -v n=4 'NR%n==1' | sed -e 's/^[ \t]*//' -e 's/^ *//g' -e 's/[[:space:]]*$//'
    '''
    posts = runshellcmd(parser)
    if len(posts) == 1:
        errlog('xinglocker: ' + 'parsing fail')
    for post in posts:
        appender(post, 'xinglocker')
    
def ragnarlocker():
    stdlog('parser: ' + 'ragnarlocker')
    json_parser = '''
    grep 'var post_links' source/ragnarlocker-*.html --no-filename | sed -e s/"        var post_links = "// -e "s/ ;//"
    '''
    posts = runshellcmd(json_parser)
    post_json = json.loads(posts[0])
    with open('source/ragnarlocker.json', 'w', encoding='utf-8') as f:
        json.dump(post_json, f, indent=4)
        f.close()
    if len(post_json) == 1:
        errlog('ragnarlocker: ' + 'parsing fail')
    for post in post_json:
        try:
            appender(post['title'], 'ragnarlocker')
        except TypeError:
            errlog('ragnarlocker: ' + 'parsing fail')

def clop():
    stdlog('parser: ' + 'clop')
    parser = '''
    grep 'PUBLISHED' source/clop-*.html --no-filename | sed -e s/"<strong>"// -e s/"<\/strong>"// -e s/"<\/p>"// -e s/"<p>"// -e s/"<br>"// -e s/"<strong>"// -e s/"<\/strong>"// -e 's/^ *//g' -e 's/[[:space:]]*$//'
    '''
    posts = runshellcmd(parser)
    if len(posts) == 1:
        errlog('clop: ' + 'parsing fail')
    for post in posts:
        appender(post, 'clop')

def revil():
    stdlog('parser: ' + 'revil')
    # grep 'href="/posts' source/revil-*.html --no-filename | cut -d '>' -f2 | sed -e s/'<\/a'// -e 's/^[ \t]*//'
    parser = '''
    grep 'justify-content-between' source/revil-*.html --no-filename | cut -d '>' -f 3 | cut -d '<' -f 1 | sed -e 's/^ *//g' -e 's/[[:space:]]*$//'
    '''
    posts = runshellcmd(parser)
    if len(posts) == 1:
        errlog('revil: ' + 'parsing fail')
    for post in posts:
        appender(post, 'revil')

def conti():
    stdlog('parser: ' + 'conti')
    # grep 'class="title">&' source/conti-*.html --no-filename | cut -d ";" -f2 | sed -e s/"&rdquo"//
    parser = '''
    grep 'newsList' source/conti-continewsnv5ot*.html --no-filename | sed -e 's/        newsList(//g' -e 's/);//g' | jq '.[].title' -r  || true
    '''
    posts = runshellcmd(parser)
    if len(posts) == 1:
        errlog('conti: ' + 'parsing fail')
    for post in posts:
        appender(post, 'conti')
    
def pysa():
    stdlog('parser: ' + 'pysa')
    parser = '''
    grep 'icon-chevron-right' source/pysa-*.html --no-filename | cut -d '>' -f3 | sed 's/^ *//g'
    '''
    posts = runshellcmd(parser)
    if len(posts) == 1:
        errlog('pysa: ' + 'parsing fail')
    for post in posts:
        appender(post, 'pysa')

def nefilim():
    stdlog('parser: ' + 'nefilim')
    parser = '''
    grep 'h2' source/nefilim-*.html --no-filename | cut -d '>' -f3 | sed -e s/'<\/a'//
    '''
    posts = runshellcmd(parser)
    if len(posts) == 1:
        errlog('nefilim: ' + 'parsing fail')
    for post in posts:
        appender(post, 'nefilim') 

def mountlocker():
    stdlog('parser: ' + 'mountlocker')
    parser = '''
    grep '<h3><a href=' source/mount-locker-*.html --no-filename | cut -d '>' -f5 | sed -e s/'<\/a'// -e 's/^ *//g' -e 's/[[:space:]]*$//'
    '''
    posts = runshellcmd(parser)
    if len(posts) == 1:
        errlog('mountlocker: ' + 'parsing fail')
    for post in posts:
        appender(post, 'mountlocker')

def babuk():
    stdlog('parser: ' + 'babuk')
    parser = '''
    grep '<h5>' source/babuk-*.html --no-filename | sed 's/^ *//g' | cut -d '>' -f2 | cut -d '<' -f1 | grep -wv 'Hospitals\|Non-Profit\|Schools\|Small Business' | sed '/^[[:space:]]*$/d'
    '''
    posts = runshellcmd(parser)
    if len(posts) == 1:
        errlog('babuk: ' + 'parsing fail')
    for post in posts:
        appender(post, 'babuk')
    
def ransomexx():
    stdlog('parser: ' + 'ransomexx')
    parser = '''
    grep 'card-title' source/ransomexx-*.html --no-filename | cut -d '>' -f2 | sed -e s/'<\/h5'// -e 's/^ *//g' -e 's/[[:space:]]*$//'
    '''
    posts = runshellcmd(parser)
    if len(posts) == 1:
        errlog('ransomexx: ' + 'parsing fail')
    for post in posts:
        appender(post, 'ransomexx')

def cuba():
    stdlog('parser: ' + 'cuba')
    # grep '<p>' source/cuba-*.html --no-filename | cut -d '>' -f3 | cut -d '<' -f1
    parser = '''
    grep '<a href="http://' source/cuba-cuba4i* | cut -d '/' -f 4 | sort -u
    '''
    posts = runshellcmd(parser)
    if len(posts) == 1:
        errlog('cuba: ' + 'parsing fail')
    for post in posts:
        appender(post, 'cuba')

def pay2key():
    stdlog('parser: ' + 'pay2key')
    parser = '''
    grep 'h3><a href' source/pay2key-*.html --no-filename | cut -d '>' -f3 | sed -e s/'<\/a'//
    '''
    posts = runshellcmd(parser)
    if len(posts) == 1:
        errlog('pay2key: ' + 'parsing fail')
    for post in posts:
        appender(post, 'pay2key')

def azroteam():
    stdlog('parser: ' + 'azroteam')
    parser = '''
    grep "h3" -A1 source/aztroteam-*.html --no-filename | grep -v h3 | awk -v n=4 'NR%n==1' | sed -e 's/^[ \t]*//'
    '''
    posts = runshellcmd(parser)
    if len(posts) == 1:
        errlog('azroteam: ' + 'parsing fail')
    for post in posts:
        appender(post, 'azroteam')

def lockdata():
    stdlog('parser: ' + 'lockdata')
    parser = '''
    grep '<a href="/view.php?' source/lockdata-*.html --no-filename | cut -d '>' -f2 | cut -d '<' -f1
    '''
    posts = runshellcmd(parser)
    if len(posts) == 1:
        errlog('lockdata: ' + 'parsing fail')
    for post in posts:
        appender(post, 'lockdata')
    
def blacktor():
    stdlog('parser: ' + 'blacktor')
    # sed -n '/tr/{n;p;}' source/bl@cktor-*.html | grep 'td' | cut -d '>' -f2 | cut -d '<' -f1
    parser = '''
    grep '>Details</a></td>' source/blacktor-*.html --no-filename | cut -f2 -d '"' | cut -f 2- -d- | cut -f 1 -d .
    '''
    posts = runshellcmd(parser)
    if len(posts) == 1:
        errlog('blacktor: ' + 'parsing fail')
    for post in posts:
        appender(post, 'blacktor')
    
def darkleakmarket():
    stdlog('parser: ' + 'darkleakmarket')
    parser = '''
    grep 'page.php' source/darkleakmarket-*.html --no-filename | sed -e 's/^[ \t]*//' | cut -d '>' -f3 | sed '/^</d' | cut -d '<' -f1 | sed -e 's/^ *//g' -e 's/[[:space:]]*$//'
    '''
    posts = runshellcmd(parser)
    if len(posts) == 1:
        errlog('darkleakmarket: ' + 'parsing fail')
    for post in posts:
        appender(post, 'darkleakmarket')

def blackmatter():
    stdlog('parser: ' + 'blackmatter')
    parser = '''
    grep '<h4 class="post-announce-name" title="' source/blackmatter-*.html --no-filename | cut -d '"' -f4 | sort -u
    '''
    posts = runshellcmd(parser)
    if len(posts) == 1:
        errlog('blackmatter: ' + 'parsing fail')
    for post in posts:
        appender(post, 'blackmatter')

def payloadbin():
    stdlog('parser: ' + 'payloadbin')
    parser = '''
    grep '<h4 class="h4' source/payloadbin-*.html --no-filename | cut -d '>' -f3 | cut -d '<' -f 1
    '''
    posts = runshellcmd(parser)
    if len(posts) == 1:
        errlog('payloadbin: ' + 'parsing fail')
    for post in posts:
        appender(post, 'payloadbin')

def groove():
    stdlog('parser: ' + 'groove')
    parser = '''
    egrep -o 'class="title">([[:alnum:]]| |\.)+</a>' source/groove-*.html | cut -d '>' -f2 | cut -d '<' -f 1
    '''
    posts = runshellcmd(parser)
    if len(posts) == 1:
        errlog('groove: ' + 'parsing fail')
    for post in posts:
        appender(post, 'groove')

def bonacigroup():
    stdlog('parser: ' + 'bonacigroup')
    parser = '''
    grep 'h5' source/bonacigroup-*.html --no-filename | cut -d '>' -f 3 | cut -d '<' -f 1
    '''
    posts = runshellcmd(parser)
    if len(posts) == 1:
        errlog('bonacigroup: ' + 'parsing fail')
    for post in posts:
        appender(post, 'bonacigroup')

def karma():
    stdlog('parser: ' + 'karma')
    parser = '''
    grep "h2" source/karma-*.html --no-filename | cut -d '>' -f 3 | cut -d '<' -f 1 | sed '/^$/d'
    '''
    posts = runshellcmd(parser)
    if len(posts) == 1:
        errlog('karma: ' + 'parsing fail')
    for post in posts:
        appender(post, 'karma')

def blackbyte():
    stdlog('parser: ' + 'blackbyte')
    # grep "h1" source/blackbyte-*.html --no-filename | cut -d '>' -f 2 | cut -d '<' -f 1 | sed -e 's/^ *//g' -e '/^$/d' -e 's/[[:space:]]*$//'
    # grep "display-4" source/blackbyte-*.html --no-filename | cut -d '>' -f 2 | cut -d '<' -f 1 | sed -e 's/^[ \t]*//' -e 's/^ *//g' -e 's/[[:space:]]*$//'
    # grep '<h1 class="h_font"' source/blackbyte-*.html | cut -d '>' -f 2 | cut -d '<' -f 1
    parser = '''
    grep --no-filename 'class="h_font"' source/blackbyte-*.html | cut -d '>' -f 2 | cut -d '<' -f 1 | sed -e 's/^ *//g' -e '/^$/d' -e 's/[[:space:]]*$//'
    '''
    posts = runshellcmd(parser)
    if len(posts) == 1:
        errlog('blackbyte: ' + 'parsing fail')
    for post in posts:
        appender(post, 'blackbyte')

def spook():
    stdlog('parser: ' + 'spook')
    parser = '''
    grep 'h2 class' source/spook-*.html --no-filename | cut -d '>' -f 3 | cut -d '<' -f 1 | sed -e 's/^ *//g' -e '/^$/d'
    '''
    posts = runshellcmd(parser)
    if len(posts) == 1:
        errlog('spook: ' + 'parsing fail')
    for post in posts:
        appender(post, 'spook')

def quantum():
    stdlog('parser: ' + 'quantum')
    parser = '''
    awk '/h2/{getline; print}' source/quantum-*.html | sed -e 's/^ *//g' -e '/<\/a>/d'
    '''
    posts = runshellcmd(parser)
    if len(posts) == 1:
        errlog('quantum: ' + 'parsing fail')
    for post in posts:
        appender(post, 'quantum')

def atomsilo():
    stdlog('parser: ' + 'atomsilo')
    parser = '''
    cat source/atomsilo-*.html | grep "h4" | cut -d '>' -f 3 | cut -d '<' -f 1 | sed -e 's/^ *//g' -e 's/[[:space:]]*$//'
    '''
    posts = runshellcmd(parser)
    if len(posts) == 1:
        errlog('atomsilo: ' + 'parsing fail')
    for post in posts:
        appender(post, 'atomsilo')
        
def lv():
    stdlog('parser: ' + 'lv')
    # %s "blog-post-title.*?</a>" source/lv-rbvuetun*.html | cut -d '>' -f 3 | cut -d '<' -f 1
    parser = '''
    jq -r '.posts[].title' source/lv-rbvuetun*.html | sed -e 's/^ *//g' -e 's/[[:space:]]*$//'
    '''
    posts = runshellcmd(parser)
    if len(posts) == 1:
        errlog('lv: ' + 'parsing fail')
    for post in posts:
        appender(post, 'lv')

def five4bb47h():
    stdlog('parser: ' + 'sabbath')
    parser = '''
    %s "aria-label.*?>" source/sabbath-*.html | cut -d '"' -f 2 | sed -e '/Search button/d' -e '/Off Canvas Menu/d' -e '/Close drawer/d' -e '/Close search modal/d' -e '/Header Menu/d' | tr "..." ' ' | grep "\S" | cat
    ''' % (fancygrep)
    posts = runshellcmd(parser)
    if len(posts) == 1:
        errlog('sabbath: ' + 'parsing fail')
    for post in posts:
        appender(post, 'sabbath')

def midas():
    stdlog('parser: ' + 'midas')
    parser = '''
    grep "/h3" source/midas-*.html --no-filename | sed -e 's/<\/h3>//' -e 's/^ *//g' -e '/^$/d' -e 's/^ *//g' -e 's/[[:space:]]*$//' -e '/^$/d'
    '''
    posts = runshellcmd(parser)
    if len(posts) == 1:
        errlog('midas: ' + 'parsing fail')
    for post in posts:
        appender(post, 'midas')

def snatch():
    stdlog('parser: ' + 'snatch')
    parser = '''
    %s "a-b-n-name.*?</div>" source/snatch-*.html | cut -d '>' -f 2 | cut -d '<' -f 1
    ''' % (fancygrep)
    posts = runshellcmd(parser)
    if len(posts) == 1:
        errlog('snatch: ' + 'parsing fail')
    for post in posts:
        appender(post, 'snatch')

def marketo():
    stdlog('parser: ' + 'marketo')
    parser = '''
    cat source/marketo-*.html | grep '<a href="/lot' | sed -e 's/^ *//g' -e '/Show more/d' -e 's/<strong>//g' | cut -d '>' -f 2 | cut -d '<' -f 1 | sed -e '/^$/d'
    '''
    posts = runshellcmd(parser)
    if len(posts) == 1:
        errlog('marketo: ' + 'parsing fail')
    for post in posts:
        appender(post, 'marketo')

def rook():
    stdlog('parser: ' + 'rook')
    parser = '''
    grep 'class="post-title"' source/rook-*.html | cut -d '>' -f 2 | cut -d '<' -f 1 | sed '/^&#34/d'
    '''
    posts = runshellcmd(parser)
    if len(posts) == 1:
        errlog('rook: ' + 'parsing fail')
    for post in posts:
        appender(post, 'rook')

def cryp70n1c0d3():
    stdlog('parser: ' + 'cryp70n1c0d3')
    parser = '''
    grep '<td class="selection"' source/cryp70n1c0d3-*.html | cut -d '>' -f 2 | cut -d '<' -f 1 | sed -e 's/^ *//g' -e 's/[[:space:]]*$//'
    '''
    posts = runshellcmd(parser)
    if len(posts) == 1:
        errlog('cryp70n1c0d3: ' + 'parsing fail')
    for post in posts:
        appender(post, 'cryp70n1c0d3')

def mosesstaff():
    stdlog('parser: ' + 'mosesstaff')
    parser = '''
    grep '<h2 class="entry-title">' source/moses-moses-staff.html -A 3 --no-filename | grep '</a>' | sed 's/^ *//g' | cut -d '<' -f 1 | sed 's/[[:space:]]*$//'
    '''
    posts = runshellcmd(parser)
    if len(posts) == 1:
        errlog('mosesstaff: ' + 'parsing fail')
    for post in posts:
        appender(post, 'mosesstaff')

def alphv():
    stdlog('parser: ' + 'alphv')
    # egrep -o 'class="mat-h2">([[:alnum:]]| |\.)+</h2>' source/alphv-*.html | cut -d '>' -f 2 | cut -d '<' -f 1
    # grep -o 'class="mat-h2">[^<>]*<\/h2>' source/alphv-*.html | cut -d '>' -f 2 | cut -d '<' -f 1 | sed -e 's/^ *//g' -e 's/[[:space:]]*$//' -e '/No articles here yet, check back later./d'
    parser = '''
    jq -r '.items[].title' source/alphv-alphvmmm27*.html | sed -e 's/^ *//g' -e 's/[[:space:]]*$//'
    '''
    posts = runshellcmd(parser)
    if len(posts) == 1:
        errlog('alphv: ' + 'parsing fail')
    for post in posts:
        appender(post, 'alphv')

def nightsky():
    stdlog('parser: ' + 'nightsky')
    parser = '''
    grep 'class="mdui-card-primary-title"' source/nightsky-*.html --no-filename | cut -d '>' -f 3 | cut -d '<' -f 1
    '''
    posts = runshellcmd(parser)
    if len(posts) == 1:
        errlog('nightsky: ' + 'parsing fail')
    for post in posts:
        appender(post, 'nightsky')

def vicesociety():
    stdlog('parser: ' + 'vicesociety')
    parser = '''
    grep '<tr><td valign="top"><br><font size="4" color="#FFFFFF"><b>' source/vicesociety-*.html --no-filename | cut -d '>' -f 6 | cut -d '<' -f 1 | sed -e '/ato District Health Boa/d' -e 's/^ *//g' -e 's/[[:space:]]*$//'
    '''
    posts = runshellcmd(parser)
    if len(posts) == 1:
        errlog('vicesociety: ' + 'parsing fail')
    for post in posts:
        appender(post, 'vicesociety')

def pandora():
    stdlog('parser: ' + 'pandora')
    parser = '''
    grep '<span class="post-title gt-c-content-color-first">' source/pandora-*.html | cut -d '>' -f 2 | cut -d '<' -f 1
    '''
    posts = runshellcmd(parser)
    if len(posts) == 1:
        errlog('pandora: ' + 'parsing fail')
    for post in posts:
        appender(post, 'pandora')

def stormous():
    stdlog('parser: ' + 'stormous')
    # grep '<p> <h3> <font color="' source/stormous-*.html | grep '</h3>' | cut -d '>' -f 4 | cut -d '<' -f 1 | sed -e 's/^ *//g' -e 's/[[:space:]]*$//'
    # grep '<h3>' source/stormous-*.html | sed -e 's/^ *//g' -e 's/[[:space:]]*$//' | grep "^<h3> <font" | cut -d '>' -f 3 | cut -d '<' -f 1 | sed 's/[[:space:]]*$//'
    parser = '''
    awk '/<h3>/{getline; print}' source/stormous-*.html | sed -e 's/^ *//g' -e 's/[[:space:]]*$//'
    '''
    posts = runshellcmd(parser)
    if len(posts) == 1:
        errlog('stormous: ' + 'parsing fail')
    for post in posts:
        appender(post, 'stormous')

def leaktheanalyst():
    stdlog('parser: ' + 'leaktheanalyst')
    parser = '''
    grep '<label class="news-headers">' source/leaktheanalyst-*.html | cut -d '>' -f 2 | cut -d '<' -f 1 | sed -e 's/Section //' -e 's/#//' -e 's/^ *//g' -e 's/[[:space:]]*$//' | sort -n | uniq
    '''
    posts = runshellcmd(parser)
    if len(posts) == 1:
        errlog('leaktheanalyst: ' + 'parsing fail')
    for post in posts:
        appender(post, 'leaktheanalyst')

def kelvinsecurity():
    stdlog('parser: ' + 'kelvinsecurity')
    parser = '''
    egrep -o '<span style="font-size:20px;">([[:alnum:]]| |\.)+</span>' source/kelvinsecurity-*.html | cut -d '>' -f 2 | cut -d '<' -f 1
    '''
    posts = runshellcmd(parser)
    if len(posts) == 1:
        errlog('kelvinsecurity: ' + 'parsing fail')
    for post in posts:
        appender(post, 'kelvinsecurity')

def blackbasta():
    stdlog('parser: ' + 'blackbasta')
    # egrep -o 'fqd.onion/\?id=([[:alnum:]]| |\.)+"' source/blackbasta-*.html | cut -d = -f 2 | cut -d '"' -f 1 | sed -e 's/^ *//g' -e 's/[[:space:]]*$//'
    parser = '''
    grep '.onion/?id=' source/blackbasta-st*.html | cut -d '>' -f 52 | cut -d '<' -f 1 | sed -e 's/\&amp/\&/g' -e 's/\&;/\&/g'
    '''
    posts = runshellcmd(parser)
    if len(posts) == 1:
        errlog('blackbasta: ' + 'parsing fail')
    for post in posts:
        appender(post, 'blackbasta')

def onyx():
    stdlog('parser: ' + 'onyx')
    parser = '''
    grep '<h6 class=' source/onyx-*.html | cut -d '>' -f 2 | cut -d '<' -f 1 | sed -e '/Connect with us/d' -e 's/^ *//g' -e 's/[[:space:]]*$//'
    '''
    posts = runshellcmd(parser)
    if len(posts) == 1:
        errlog('onyx: ' + 'parsing fail')
    for post in posts:
        appender(post, 'onyx')

def mindware():
    stdlog('parser: ' + 'mindware')
    parser = '''
    grep '<div class="card-header">' source/mindware-*.html | cut -d '>' -f 2 | cut -d '<' -f 1
    '''
    posts = runshellcmd(parser)
    if len(posts) == 1:
        errlog('mindware: ' + 'parsing fail')
    for post in posts:
        appender(post, 'mindware')

def ransomhouse():
    stdlog('parser: ' + 'ransomhouse')
    parser = '''
    egrep -o 'class="cls_recordTop"><p>([[:alnum:]]| |\.)+</p>' source/ransomhouse-*.html | cut -d '>' -f 3 | cut -d '<' -f 1
    '''
    posts = runshellcmd(parser)
    if len(posts) == 1:
        errlog('ransomhouse: ' + 'parsing fail')
    for post in posts:
        appender(post, 'ransomhouse')

def cheers():
    stdlog('parser: ' + 'cheers')
    parser = '''
    cat  source/cheers-*.html | grep '<a href="' | grep -v title | cut -d '>' -f 2 | cut -d '<' -f 1 | sed -e '/Cheers/d' -e '/Home/d' -e 's/^ *//g' -e 's/[[:space:]]*$//'
    '''
    posts = runshellcmd(parser)
    if len(posts) == 1:
        errlog('cheers: ' + 'parsing fail')
    for post in posts:
        appender(post, 'cheers')

def lockbit3():
    stdlog('parser: ' + 'lockbit3')
    parser = '''
    grep '<div class="post-title">' source/lockbit3-*.html -C 1 --no-filename | grep '</div>' | cut -d '<' -f 1 | sed -e 's/^ *//g' -e 's/[[:space:]]*$//' | sort --uniq
    '''
    posts = runshellcmd(parser)
    if len(posts) == 1:
        errlog('lockbit3: ' + 'parsing fail')
    for post in posts:
        appender(post, 'lockbit3')

def yanluowang():
    stdlog('parser: ' + 'yanluowang')
    parser = '''
    grep '<a href="/posts' source/yanluowang-*.html | cut -d '>' -f 2 | cut -d '<' -f 1 | sed -e 's/^ *//g' -e 's/[[:space:]]*$//'
    '''
    posts = runshellcmd(parser)
    if len(posts) == 1:
        errlog('yanluowang: ' + 'parsing fail')
    for post in posts:
        appender(post, 'yanluowang')

def omega():
    stdlog('parser: ' + '0mega')
    parser = '''
    grep "<tr class='trow'>" -C 1 source/0mega-*.html | grep '<td>' | cut -d '>' -f 2 | cut -d '<' -f 1 | sort --uniq
    '''
    posts = runshellcmd(parser)
    if len(posts) == 1:
        errlog('0mega: ' + 'parsing fail')
    for post in posts:
        appender(post, '0mega')

def bianlian():
    stdlog('parser: ' + 'bianlian')
    parser = '''
    sed -n '/<a href="\/companies\//,/<\/a>/p' source/bianlian-*.html | egrep -o '([[:alnum:]]| |\.)+</a>' | cut -d '<' -f 1 | sed -e '/Contacts/d'
    '''
    posts = runshellcmd(parser)
    if len(posts) == 1:
        errlog('bianlian: ' + 'parsing fail')
    for post in posts:
        appender(post, 'bianlian')

def redalert():
    stdlog('parser: ' + 'redalert')
    parser = '''
    egrep -o '<h3>([[:alnum:]]| |\.)+</h3>' source/redalert-*.html | cut -d '>' -f 2 | cut -d '<' -f 1
    '''
    posts = runshellcmd(parser)
    if len(posts) == 1:
        errlog('redalert: ' + 'parsing fail')
    for post in posts:
        appender(post, 'redalert')

def daixin():
    stdlog('parser: ' + 'daixin')
    parser = '''
    grep '<h4 class="border-danger' source/daixin-*.html | cut -d '>' -f 3 | cut -d '<' -f 1 | sed -e 's/^ *//g' -e '/^$/d' -e 's/[[:space:]]*$//'
    '''
    posts = runshellcmd(parser)
    if len(posts) == 1:
        errlog('daixin: ' + 'parsing fail')
    for post in posts:
        appender(post, 'daixin')

def icefire():
    stdlog('parser: ' + 'icefire')
    parser = '''
    grep align-middle -C 2 source/icefire-*.html | grep span | grep -v '\*\*\*\*' | grep -v updating | grep '\*\.' | cut -d '>' -f 2 | cut -d '<' -f 1
    '''
    posts = runshellcmd(parser)
    if len(posts) == 1:
        errlog('icefire: ' + 'parsing fail')
    for post in posts:
        appender(post, 'icefire')

def donutleaks():
    stdlog('parser: ' + 'donutleaks')
    parser = '''
    grep '<h2 class="post-title">' source/donutleaks-*.html --no-filename | cut -d '>' -f 3 | cut -d '<' -f 1
    '''
    posts = runshellcmd(parser)
    if len(posts) == 1:
        errlog('donutleaks: ' + 'parsing fail')
    for post in posts:
        appender(post, 'donutleaks')
