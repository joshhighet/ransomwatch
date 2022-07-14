#!/bin/zsh
# freshonifyfe4rmuh6qwpsexfhdrww7wnt5qmkoertwxmcuvm4woo4ad.onion
# onionwsoiu53xre32jwve7euacadvhprq2jytfttb55hrbo3execodad.onion

set -e

if ! `nc -z localhost 9050`; then
    echo "localhost:9050 socksproxy required!"
    exit 1
fi

random_useragent=`cat assets/useragents.txt | shuf -n 1`

if [ ! -d assets/tmp ]; then
    mkdir assets/tmp
fi

dnet_tgram=`curl -s --socks5-hostname localhost:9050 lpnxgtkni46pngdg4pml47hvxg2xqdcrd7z2f5oysyuialodho6g34yd.onion -H 'User-Agent: '${random_useragent}''`
if [ $? -ne 0 ]; then
    echo "failed to fetch from telegram:dbforall"
    exit 1
fi
echo ${dnet_tgram} | sed -E -e 's_.*://([^/@]*@)?([^/:]+).*_\2_' | grep onion | cut -d '"' -f 1 > assets/tmp/sources.dnet_tgram
dnet_tgram_count=`cat assets/tmp/sources.dnet_tgram | wc -w | awk '{$1=$1};1'`
echo "${dnet_tgram_count} | telegram:dbforall"

googlesheCZJ=`curl -s 'https://docs.google.com/spreadsheets/d/1cH4KCZJvggoHPAbk0u08Wu1vSo9ygx47QfhKD-W0TQ0/gviz/tq?tqx=out:csv' -H 'User-Agent: '${random_useragent}''`
if [ $? -ne 0 ]; then
    echo "failed to fetch from googlesheets:1cH4KCZJ"
    exit 1
fi
echo $googlesheCZJ | cut -d ',' -f 3 | grep onion | sed -E -e 's/^[[:space:]]*//' -e 's/^"//' -e 's/"$//' -e 's:/*$::' -e 's/onion.ly/onion/g' -e 's/http:\/\///' -e 's/https:\/\///' | cut -f1 -d"/" > assets/tmp/sources.googlesheCZJ
googlesheCZJ_count=`cat assets/tmp/sources.googlesheCZJ | wc -w | awk '{$1=$1};1'`
echo "${googlesheCZJ_count} | googlesheets:1cH4KCZJ"

rgs=`curl -s --socks5-hostname localhost:9050 ransomwr3tsydeii4q43vazm7wofla5ujdajquitomtd47cxjtfgwyyd.onion -H 'User-Agent: '${random_useragent}''`
if [ $? -ne 0 ]; then
    echo "failed to fetch from onion:ransomwr3"
    exit 1
fi
echo ${rgs} | sed -E -e 's_.*://([^/@]*@)?([^/:]+).*_\2_' | grep onion | cut -d '"' -f 1 > assets/tmp/sources.rgs
rgs_count=`cat assets/tmp/sources.rgs | wc -w | awk '{$1=$1};1'`
echo "${rgs_count} | onion:ransomwr3"

ddcti_ransomgang=`curl -s https://raw.githubusercontent.com/fastfire/deepdarkCTI/main/ransomware_gang.md  -H 'User-Agent: '${random_useragent}''`
if [ $? -ne 0 ]; then
    echo "failed to fetch from github:deepdarkCTI:ransomgang"
    exit 1
fi
echo ${ddcti_ransomgang} | sed -E -e 's_.*://([^/@]*@)?([^/:]+).*_\2_' | grep onion | cut -d ' ' -f 1 | cut -d '|' -f 1 > assets/tmp/sources.ddcti_ransomgang
ddcti_ransomgang_count=`cat assets/tmp/sources.ddcti_ransomgang | wc -w | awk '{$1=$1};1'`
echo "${ddcti_ransomgang_count} | github:deepdarkCTI:ransomgang"

ddcti_maas=`curl -s https://raw.githubusercontent.com/fastfire/deepdarkCTI/main/maas.md -H 'User-Agent: '${random_useragent}''`
if [ $? -ne 0 ]; then
    echo "failed to fetch from github:deepdarkCTI:maas"
    exit 1
fi
echo ${ddcti_maas} | sed -E -e 's_.*://([^/@]*@)?([^/:]+).*_\2_' | grep onion | cut -d ' ' -f 1 | cut -d '|' -f 1 > assets/tmp/sources.ddcti_maas
ddcti_maas_count=`cat assets/tmp/sources.ddcti_maas | wc -w | awk '{$1=$1};1'`
echo "${ddcti_maas_count} | github:deepdarkCTI:maas"

ddcti_markets=`curl -s https://raw.githubusercontent.com/fastfire/deepdarkCTI/main/markets.md -H 'User-Agent: '${random_useragent}''`
if [ $? -ne 0 ]; then
    echo "failed to fetch from github:deepdarkCTI:markets"
    exit 1
fi
echo ${ddcti_markets} | sed -E -e 's_.*://([^/@]*@)?([^/:]+).*_\2_' | grep onion | cut -d ' ' -f 1 | cut -d '|' -f 1 > assets/tmp/sources.ddcti_markets
ddcti_markets_count=`cat assets/tmp/sources.ddcti_markets | wc -w | awk '{$1=$1};1'`
echo "${ddcti_markets_count} | github:deepdarkCTI:markets"

ddcti_forum=`curl -s https://raw.githubusercontent.com/fastfire/deepdarkCTI/main/forum.md -H 'User-Agent: '${random_useragent}''`
if [ $? -ne 0 ]; then
    echo "failed to fetch from github:deepdarkCTI:forum"
    exit 1
fi
echo ${ddcti_forum} | sed -E -e 's_.*://([^/@]*@)?([^/:]+).*_\2_' | grep onion | cut -d ' ' -f 1 | cut -d '|' -f 1 > assets/tmp/sources.ddcti_forum
ddcti_forum_count=`cat assets/tmp/sources.ddcti_forum | wc -w | awk '{$1=$1};1'`
echo "${ddcti_forum_count} | github:deepdarkCTI:forum"

gistteix=`curl -s https://gist.githubusercontent.com/teixeira0xfffff/3ac8d9c4bf113e56533299b2da8c856b/raw/4e70ff99a7af2a86f720de65d5218f7b9c9f21d0/ransomwarefeed.csv -H 'User-Agent: '${random_useragent}''`
if [ $? -ne 0 ]; then
    echo "failed to fetch from gist:teixeira0xfffff:ransomwarefeed.csv"
    exit 1
fi
echo ${gistteix} | cut -d ',' -f 2 | sed -E -e 's_.*://([^/@]*@)?([^/:]+).*_\2_' > assets/tmp/sources.gistteix
gistteix_count=`cat assets/tmp/sources.gistteix | wc -w | awk '{$1=$1};1'`
echo "${gistteix_count} | gist:teixeira0xfffff:ransomwarefeed.csv"

lpn=`curl -s --socks5-hostname localhost:9050 lpnxgtkni46pngdg4pml47hvxg2xqdcrd7z2f5oysyuialodho6g34yd.onion -H 'User-Agent: '${random_useragent}''`
if [ $? -ne 0 ]; then
    echo "failed to fetch from onion:lpnxgtkni"
    exit 1
fi
echo ${lpn} | sed -E -e 's_.*://([^/@]*@)?([^/:]+).*_\2_' | grep onion | cut -d '"' -f 1 > assets/tmp/sources.lpn
lpn_count=`cat assets/tmp/sources.lpn | wc -w | awk '{$1=$1};1'`
echo "${lpn_count} | onion:lpnxgtkni"

#inh=`curl -s --socks5-hostname localhost:9050 inhx4x4y66guy6ljnhq3ijbbgroha5sejcyo2uejmzv6vd3ydwzc6fid.onion -H 'User-Agent: '${random_useragent}''`
#if [ $? -ne 0 ]; then
#    echo "failed to fetch from onion:inhx4x4y6"
#    exit 1
#fi
#echo ${inh} | sed -E -e 's_.*://([^/@]*@)?([^/:]+).*_\2_' | grep onion | cut -d '"' -f 1 > assets/tmp/sources.inh
#inh_count=`cat assets/tmp/sources.inh | wc -w | awk '{$1=$1};1'`
#echo "${inh_count} | onion:inhx4x4y6"

cat assets/tmp/sources.* | sort | uniq | tr '[:upper:]' '[:lower:]' | grep -Eo '^([a-z0-9][a-z0-9_-]*\.)*[a-z2-7]{56}\.onion' | while read host;
do
    if ! grep -q "${host}" assets/sources.exclusions && ! grep -q "${host}" groups.json; then
        echo "${host}"
    fi
done <<< "${hosts}"
#rm assets/tmp/sources.*
