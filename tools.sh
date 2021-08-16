#!/bin/bash
# theta.co.nz/cyber

set -e

# https://stackoverflow.com/questions/1732348/regex-match-open-tags-except-xhtml-self-contained-tags/1732454#1732454

######
# beautifulsoup would be a cleaner implementation but comes w/ setup grief
# 
# from bs4 import BeautifulSoup
# 
# def soupinit(file):
#     htmldoc = sharedutils.openhtml(file)
#     soup = BeautifulSoup(htmldoc, 'html.parser')
#     return soup
# 
# def arvinclub(doc):
#     soup = soupinit(doc)
#     headers = soup.find_all('h2')
#     for head in headers:
#         part = str(head).partition('bookmark">')[2]
#         title = part.strip('</a></h2>')
#         print(title)
# 
# arvinclub('source/arvinclub.html')
######

if [ "$1" == "parser" ]; then
    ###💀😵‍💫✨
    # marketo
    # dead
    ###💀😵‍💫✨
    # synack
    grep 'card-title' source/synack*.html \
    | cut -d ">" -f2 \
    | cut -d "<" -f1 \
    | tee -a normalised/synack.txt
    sort -u normalised/synack.txt | uniq > normalised/synack.sorted.txt
    mv normalised/synack.sorted.txt normalised/synack.txt
    ###💀😵‍💫✨
    # suncrypt
    cat source/suncrypt-*.html \
    | tr '>' '\n' \
    | grep -A1 '<a href="client?id=' \
    | sed '/^--/d' \
    | sed '/^<a/d' \
    | cut -d '<' -f1 \
    | tee -a normalised/suncrypt.txt
    sort -u normalised/suncrypt.txt | uniq > normalised/suncrypt.sorted.txt
    mv normalised/suncrypt.sorted.txt normalised/suncrypt.txt
    ###💀😵‍💫✨
    # lv
    # uses javascript
    ###💀😵‍💫✨
    # lorenz
    grep 'h3' source/lorenz*.html \
    | cut -d ">" -f2 \
    | cut -d "<" -f1 \
    | sed -e 's/^ *//g' -e '/^$/d' \
    | tee -a normalised/lorenz.txt
    sort -u normalised/lorenz.txt | uniq > normalised/lorenz.sorted.txt
    mv normalised/lorenz.sorted.txt normalised/lorenz.txt
    ###💀😵‍💫✨
    # lockbit2
    ## titles
    awk '/<div class=post-title>/{getline; print}' source/lockbit2*.html \
    | cut -d '<' -f1 \
    | tee -a normalised/lockbit2.txt
    sort -u normalised/lockbit2.txt | uniq > normalised/lockbit2.sorted.txt
    mv normalised/lockbit2.sorted.txt normalised/lockbit2.txt
    ## descriptions
        # sed -n '/post-block-text/{n;p;}' source/lockbit2*.html \
        # | sed '/^</d' \
        # | cut -d "<" -f1 \
        # | tee -a normalised/lockbit2.txt
        # sort -u normalised/lockbit2.txt | uniq > normalised/lockbit2.sorted.txt
        # mv normalised/lockbit2.sorted.txt normalised/lockbit2.txt
    ###💀😵‍💫✨
    # hive
    # uses javascript
    ###💀😵‍💫✨
    # arvinclub
    grep 'bookmark' source/arvinclub*.html \
    | cut -d ">" -f3 \
    | cut -d "<" -f1 \
    | tee -a normalised/arvinclub.txt
    sort -u normalised/arvinclub.txt | uniq > normalised/arvinclub.sorted.txt
    mv normalised/arvinclub.sorted.txt normalised/arvinclub.txt
    ###💀😵‍💫✨
    # avoslocker
    sed -n -e 's/^.*aria-hidden="true"><\/i> //p' source/avoslocker-*.html \
    | cut -d "<" -f1 \
    | tee -a normalised/avoslocker.txt
    sort -u normalised/avoslocker.txt | uniq > normalised/avoslocker.sorted.txt
    mv normalised/avoslocker.sorted.txt normalised/avoslocker.txt
    ###💀😵‍💫✨
    # grief
    # uses javascript
    ###💀😵‍💫✨
    # avaddon
    grep 'h6' source/avaddon*.html \
    | cut -d ">" -f3 \
    | sed -e s/'<\/a'// \
    | tee -a normalised/avaddon.txt
    sort -u normalised/avaddon.txt | uniq > normalised/avaddon.sorted.txt
    mv normalised/avaddon.sorted.txt normalised/avaddon.txt
    ###💀😵‍💫✨
    # vicesociety
    # dead
    ###💀😵‍💫✨
    # xinglocker
    grep "h3" -A1 source/xinglocker*.html \
    | grep -v h3 \
    | awk -v n=4 'NR%n==1' \
    | sed -e 's/^[ \t]*//' \
    | tee -a normalised/xinglocker.txt
    sort -u normalised/xinglocker.txt | uniq > normalised/xinglocker.sorted.txt
    mv normalised/xinglocker.sorted.txt normalised/xinglocker.txt
    ###💀😵‍💫✨
    # darkside
    # dead
    ###💀😵‍💫✨
    # ragnarlocker - has json within html source so fetch & postprocess w/ jq
    grep 'var post_links' source/ragnarlocker*.html \
    | sed -e s/"        var post_links = "// -e "s/ ;//" \
    | jq > source/ragnarlocker.json
    jq -r '.[].title' source/ragnarlocker.json \
    | tee -a normalised/ragnarlocker.txt
    sort -u normalised/ragnarlocker.txt | uniq > normalised/ragnarlocker.sorted.txt
    mv normalised/ragnarlocker.sorted.txt normalised/ragnarlocker.txt
    ###💀😵‍💫✨
    # clop
    grep 'PUBLISHED' source/clop*.html \
    | sed -e s/"<strong>"// -e s/"<\/strong>"// -e s/"<\/p>"// \
    -e s/"<p>"// -e s/"<br>"// -e s/"<strong>"// -e s/"<\/strong>"// \
    | tee -a normalised/clop.txt
    sort -u normalised/clop.txt | uniq > normalised/clop.sorted.txt
    mv normalised/clop.sorted.txt normalised/clop.txt
    ###💀😵‍💫✨
    # netwalker
    # dead
    ###💀😵‍💫✨
    # doppelpaymer
    # uses javascript
    ###💀😵‍💫✨
    # revil
    grep 'href="/posts' source/revil*.html \
    | cut -d '>' -f2 \
    | sed -e s/'<\/a'// -e 's/^[ \t]*//' \
    | tee -a normalised/revil.txt
    sort -u normalised/revil.txt | uniq > normalised/revil.sorted.txt
    mv normalised/revil.sorted.txt normalised/revil.txt
    ###💀😵‍💫✨
    # everest
    # dead
    ###💀😵‍💫✨
    # ragnarok
    # dead
    ###💀😵‍💫✨
    # conti
    grep 'class="title">&' source/conti*.html \
    | cut -d ";" -f2 \
    | sed -e s/"&rdquo"// \
    | tee -a normalised/conti.txt
    sort -u normalised/conti.txt | uniq > normalised/conti.sorted.txt
    mv normalised/conti.sorted.txt normalised/conti.txt
    ###💀😵‍💫✨
    # pysa
    grep 'icon-chevron-right' source/pysa*.html \
    | cut -d '>' -f3 \
    | sed 's/^ *//g' \
    | tee -a normalised/pysa.txt
    sort -u normalised/pysa.txt | uniq > normalised/pysa.sorted.txt
    mv normalised/pysa.sorted.txt normalised/pysa.txt
    ###💀😵‍💫✨
    #nefilim
    grep 'h2' source/nefilim*.html \
    | cut -d '>' -f3 \
    | sed -e s/'<\/a'// \
    | tee -a normalised/nefilim.txt
    sort -u normalised/nefilim.txt | uniq > normalised/nefilim.sorted.txt
    mv normalised/nefilim.sorted.txt normalised/nefilim.txt
    ###💀😵‍💫✨
    # maze
    # dead
    ###💀😵‍💫✨
    # mount locker
    grep '<h3><a href=' source/mount-locker*.html \
    | cut -d '>' -f5 \
    | sed -e s/'<\/a'// \
    | sed 's/^ *//g' \
    | tee -a normalised/mount-locker.txt
    sort -u normalised/mount-locker.txt | uniq > normalised/mount-locker.sorted.txt
    mv normalised/mount-locker.sorted.txt normalised/mount-locker.txt
    ###💀😵‍💫✨
    # babuk 
    # https://github.com/thetanz/ransomwatch/issues/7
    ###💀😵‍💫✨
    # ransomexx
    grep 'card-title' source/ransomexx*.html \
    | cut -d '>' -f2 \
    | sed -e s/'<\/h5'// \
    | tee -a normalised/ransomexx.txt
    sort -u normalised/ransomexx.txt | uniq > normalised/ransomexx.sorted.txt
    mv normalised/ransomexx.sorted.txt normalised/ransomexx.txt
    ###💀😵‍💫✨
    # cuba
    grep '<p>' source/cuba*.html \
    | cut -d '>' -f3 \
    | cut -d '<' -f1 \
    | tee -a normalised/cuba.txt
    sort -u normalised/cuba.txt | uniq > normalised/cuba.sorted.txt
    mv normalised/cuba.sorted.txt normalised/cuba.txt
    ###💀😵‍💫✨
    # pay2key
    grep 'h3><a href' source/pay2key*.html \
    | cut -d '>' -f3 \
    | sed -e s/'<\/a'// \
    | tee -a normalised/pay2key.txt
    sort -u normalised/pay2key.txt | uniq > normalised/pay2key.sorted.txt
    mv normalised/pay2key.sorted.txt normalised/pay2key.txt
    ###💀😵‍💫✨
    # azroteam
    grep "h3" -A1 source/aztroteam*.html \
    | grep -v h3 \
    | awk -v n=4 'NR%n==1' \
    | sed -e 's/^[ \t]*//' \
    | tee -a normalised/aztroteam.txt
    sort -u normalised/aztroteam.txt | uniq > normalised/aztroteam.sorted.txt
    mv normalised/aztroteam.sorted.txt normalised/aztroteam.txt
    ###💀😵‍💫✨
    # lockdata
    grep '<a href="/view.php?' source/lockdata-*.html \
    | cut -d '>' -f2 \
    | cut -d '<' -f1 \
    | tee -a normalised/lockdata.txt
    sort -u normalised/lockdata.txt | uniq > normalised/lockdata.sorted.txt
    mv normalised/lockdata.sorted.txt normalised/lockdata.txt
    ###💀😵‍💫✨
    # bl@cktor
    sed -n '/tr/{n;p;}' source/bl@cktor-*.html \
    | grep 'td' \
    | cut -d '>' -f2 \
    | cut -d '<' -f1 \
    | tee -a normalised/bl@cktor.txt
    sort -u normalised/bl@cktor.txt | uniq > normalised/bl@cktor.sorted.txt
    mv normalised/bl@cktor.sorted.txt normalised/bl@cktor.txt
    ###💀😵‍💫✨
    # haron
    # does not have a vlog
    ###💀😵‍💫✨
    # darkleakmarket
    grep 'page.php' source/darkleakmarket-*.html \
    | sed -e 's/^[ \t]*//' \
    | cut -d '>' -f3 \
    | sed '/^</d' \
    |  cut -d '<' -f1 \
    | tee -a normalised/darkleakmarket.txt
    sort -u normalised/darkleakmarket.txt | uniq > normalised/darkleakmarket.sorted.txt
    mv normalised/darkleakmarket.sorted.txt normalised/darkleakmarket.txt
    ###💀😵‍💫✨
elif [ "$1" == "markdown" ]; then

echo """> groups may have multiple sites or mirrors. multiple reports for a single group are expected

| group | online | last seen  | last update |
|-------|--------|------------|-------------|""" > report.md

    groups=`jq '.[].name' -r groups.json`

    for group in ${groups}
    do
        groupdata=`jq -r '.[] | select(.name=="'${group}'")' groups.json`
        groupname=`echo ${groupdata} | jq -r .name`
        availability=`echo ${groupdata} | jq -r .locations[].available`
        lastscrapetz=`echo ${groupdata} | jq -r .locations[].lastscrape`
        lastupdatetz=`echo ${groupdata} | jq -r .locations[].updated`
        echo '| '${groupname}' | '${availability}' | '${lastscrapetz}' | '${lastupdatetz}' |' >> report.md
    done

else
   echo "mode must be specified (parser or markdown)!"
fi