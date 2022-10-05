#!/bin/zsh
# freshonifyfe4rmuh6qwpsexfhdrww7wnt5qmkoertwxmcuvm4woo4ad.onion
# onionwsoiu53xre32jwve7euacadvhprq2jytfttb55hrbo3execodad.onion

# PROBE=TRUE ./sources.zsh --socks5 telemetry.dark:9050

#set -ex

SOCKS5_PROXY=localhost:9050
if [[ $1 == "--socks5" ]]; then
  SOCKS5_PROXY=$2
  shift 2
fi

SOCKSHOST=$(echo $SOCKS5_PROXY | cut -d: -f1)
SOCKSPORT=$(echo $SOCKS5_PROXY | cut -d: -f2)

# check darwin
if [[ $(uname) != "Darwin" ]]; then
  echo "script untested outside of macos"
  exit
fi

if ! nc -z ${SOCKSHOST} ${SOCKSPORT} 2>/dev/null; then
  echo "${SOCKS5_PROXY} is not accepting connections"
  if [[ $1 != "--socks5" ]]; then
    echo "specify an alternate proxy with --socks5 proxy.local:9050"
    echo "i.e ./sources.zsh --socks5 tor.local:9050"
  fi
  exit 1
fi

random_useragent=`cat assets/useragents.txt | shuf -n 1`

if [ ! -d assets/tmp ]; then
    mkdir assets/tmp
fi

dnet_tgram=`curl -s --socks5-hostname ${SOCKS5_PROXY} https://telemetr.io/en/channels/1232665535-dbforall/posts -H 'User-Agent: '${random_useragent}''`
echo "fetching: telegram:dbforall"
echo $dnet_tgram > /tmp/dnet_tgram.html
if [ $? -ne 0 ]; then
    echo "failed to fetch from telegram:dbforall"
fi
echo ${dnet_tgram} | grep -Eo "(http|https)://[a-zA-Z0-9./?=_%:-]*" | grep onion | sed -E -e 's_.*://([^/@]*@)?([^/:]+).*_\2_' -e 's/\.$//' | sort -u > assets/tmp/sources.dnet_tgram
dnet_tgram_count=`cat assets/tmp/sources.dnet_tgram | wc -w | awk '{$1=$1};1'`
echo "${dnet_tgram_count} | telegram:dbforall"

googlesheCZJ=`curl -s 'https://docs.google.com/spreadsheets/d/1cH4KCZJvggoHPAbk0u08Wu1vSo9ygx47QfhKD-W0TQ0/gviz/tq?tqx=out:csv' -H 'User-Agent: '${random_useragent}''`
echo "fetching: google:sheets:1cH4KCZJvggoHPAbk0u08Wu1vSo9ygx47QfhKD-W0TQ0"
echo $googlesheCZJ > /tmp/googlesheCZJ.csv
if [ $? -ne 0 ]; then
    echo "failed to fetch from googlesheets:1cH4KCZJ"
fi
echo $googlesheCZJ | cut -d ',' -f 3 | grep onion | sed -E -e 's/^[[:space:]]*//' -e 's/^"//' -e 's/"$//' -e 's:/*$::' -e 's/onion.ly/onion/g' -e 's/http:\/\///' -e 's/https:\/\///' | cut -f1 -d"/" > assets/tmp/sources.googlesheCZJ
googlesheCZJ_count=`cat assets/tmp/sources.googlesheCZJ | wc -w | awk '{$1=$1};1'`
echo "${googlesheCZJ_count} | googlesheets:1cH4KCZJ"

rgs=`curl -s --socks5-hostname ${SOCKS5_PROXY} ransomwr3tsydeii4q43vazm7wofla5ujdajquitomtd47cxjtfgwyyd.onion -H 'User-Agent: '${random_useragent}''`
echo "fetching: onion:ransomwr3tsy"
echo $rgs > /tmp/ransomwr3tsy.html
if [ $? -ne 0 ]; then
    echo "failed to fetch from onion:ransomwr3"
fi
echo ${rgs} | sed -E -e 's_.*://([^/@]*@)?([^/:]+).*_\2_' | grep onion | cut -d '"' -f 1 > assets/tmp/sources.rgs
rgs_count=`cat assets/tmp/sources.rgs | wc -w | awk '{$1=$1};1'`
echo "${rgs_count} | onion:ransomwr3"

ddcti_ransomgang=`curl -s https://raw.githubusercontent.com/fastfire/deepdarkCTI/main/ransomware_gang.md  -H 'User-Agent: '${random_useragent}''`
echo "fetching: ddcti:ransomgang"
echo $ddcti_ransomgang > /tmp/ddcti_ransomgang.md
if [ $? -ne 0 ]; then
    echo "failed to fetch from github:deepdarkCTI:ransomgang"
fi
echo ${ddcti_ransomgang} | sed -E -e 's_.*://([^/@]*@)?([^/:]+).*_\2_' | grep onion | cut -d ' ' -f 1 | cut -d '|' -f 1 > assets/tmp/sources.ddcti_ransomgang
ddcti_ransomgang_count=`cat assets/tmp/sources.ddcti_ransomgang | wc -w | awk '{$1=$1};1'`
echo "${ddcti_ransomgang_count} | github:deepdarkCTI:ransomgang"

ddcti_maas=`curl -s https://raw.githubusercontent.com/fastfire/deepdarkCTI/main/maas.md -H 'User-Agent: '${random_useragent}''`
echo "fetching: ddcti:maas"
echo $ddcti_maas > /tmp/ddcti_maas.md
if [ $? -ne 0 ]; then
    echo "failed to fetch from github:deepdarkCTI:maas"
fi
echo ${ddcti_maas} | sed -E -e 's_.*://([^/@]*@)?([^/:]+).*_\2_' | grep onion | cut -d ' ' -f 1 | cut -d '|' -f 1 > assets/tmp/sources.ddcti_maas
ddcti_maas_count=`cat assets/tmp/sources.ddcti_maas | wc -w | awk '{$1=$1};1'`
echo "${ddcti_maas_count} | github:deepdarkCTI:maas"

ddcti_markets=`curl -s https://raw.githubusercontent.com/fastfire/deepdarkCTI/main/markets.md -H 'User-Agent: '${random_useragent}''`
echo "fetching: ddcti:markets"
echo $ddcti_markets > /tmp/ddcti_markets.md
if [ $? -ne 0 ]; then
    echo "failed to fetch from github:deepdarkCTI:markets"
fi
echo ${ddcti_markets} | sed -E -e 's_.*://([^/@]*@)?([^/:]+).*_\2_' | grep onion | cut -d ' ' -f 1 | cut -d '|' -f 1 > assets/tmp/sources.ddcti_markets
ddcti_markets_count=`cat assets/tmp/sources.ddcti_markets | wc -w | awk '{$1=$1};1'`
echo "${ddcti_markets_count} | github:deepdarkCTI:markets"

ddcti_forum=`curl -s https://raw.githubusercontent.com/fastfire/deepdarkCTI/main/forum.md -H 'User-Agent: '${random_useragent}''`
echo "fetching: ddcti:forum"
echo $ddcti_forum > /tmp/ddcti_forum.md
if [ $? -ne 0 ]; then
    echo "failed to fetch from github:deepdarkCTI:forum"
fi
echo ${ddcti_forum} | sed -E -e 's_.*://([^/@]*@)?([^/:]+).*_\2_' | grep onion | cut -d ' ' -f 1 | cut -d '|' -f 1 > assets/tmp/sources.ddcti_forum
ddcti_forum_count=`cat assets/tmp/sources.ddcti_forum | wc -w | awk '{$1=$1};1'`
echo "${ddcti_forum_count} | github:deepdarkCTI:forum"

gistteix=`curl -s https://gist.githubusercontent.com/teixeira0xfffff/3ac8d9c4bf113e56533299b2da8c856b/raw/4e70ff99a7af2a86f720de65d5218f7b9c9f21d0/ransomwarefeed.csv -H 'User-Agent: '${random_useragent}''`
echo "fetching: gist:teixeira0xfffff"
echo $gistteix > /tmp/gistteix.csv
if [ $? -ne 0 ]; then
    echo "failed to fetch from gist:teixeira0xfffff:ransomwarefeed.csv"
fi
echo ${gistteix} | cut -d ',' -f 2 | sed -E -e 's_.*://([^/@]*@)?([^/:]+).*_\2_' > assets/tmp/sources.gistteix
gistteix_count=`cat assets/tmp/sources.gistteix | wc -w | awk '{$1=$1};1'`
echo "${gistteix_count} | gist:teixeira0xfffff:ransomwarefeed.csv"

breachsense=`curl -s https://www.breachsense.io/ransomware-gangs/ -H 'User-Agent: '${random_useragent}''`
echo "fetching: breachsense"
echo $breachsense > /tmp/breachsense.html
if [ $? -ne 0 ]; then
    echo "failed to fetch from breachsense.io"
fi
echo ${breachsense} | sed -E -e 's_.*://([^/@]*@)?([^/:]+).*_\2_' | grep onion | cut -d '>' -f 1 | sed 's/onion.ws/onion/g' > assets/tmp/sources.breachsense
breachsense_count=`cat assets/tmp/sources.breachsense | wc -w | awk '{$1=$1};1'`
echo "${breachsense_count} | breachsense"

lpn=`curl -s --socks5-hostname ${SOCKS5_PROXY} lpnxgtkni46pngdg4pml47hvxg2xqdcrd7z2f5oysyuialodho6g34yd.onion -H 'User-Agent: '${random_useragent}''`
echo "fetching: lpn"
echo $lpn > /tmp/lpn.html
if [ $? -ne 0 ]; then
    echo "failed to fetch from onion:lpnxgtkni"
fi
echo ${lpn} | sed -E -e 's_.*://([^/@]*@)?([^/:]+).*_\2_' | grep onion | cut -d '"' -f 1 > assets/tmp/sources.lpn
lpn_count=`cat assets/tmp/sources.lpn | wc -w | awk '{$1=$1};1'`
echo "${lpn_count} | onion:lpnxgtkni"

inh=`curl -s --socks5-hostname ${SOCKS5_PROXY} inhx4x4y66guy6ljnhq3ijbbgroha5sejcyo2uejmzv6vd3ydwzc6fid.onion -H 'User-Agent: '${random_useragent}''`
echo "fetching: inh"
echo $inh > /tmp/inh.html
if [ $? -ne 0 ]; then
    echo "failed to fetch from onion:inhx4x4y6"
fi
echo ${inh} | sed -E -e 's_.*://([^/@]*@)?([^/:]+).*_\2_' | grep onion | cut -d '"' -f 1 > assets/tmp/sources.inh
inh_count=`cat assets/tmp/sources.inh | wc -w | awk '{$1=$1};1'`
echo "${inh_count} | onion:inhx4x4y6"

cat assets/tmp/sources.* | sort | uniq | tr '[:upper:]' '[:lower:]' | grep -Eo '^([a-z0-9][a-z0-9_-]*\.)*[a-z2-7]{56}\.onion' | while read host;
do
    if ! grep -q "${host}" assets/sources.exclusions && ! grep -q "${host}" groups.json; then
        if [ "${PROBE}" = "TRUE" ]; then
            checksrc=$(timeout 10 curl -sL --socks5-hostname ${SOCKS5_PROXY} ${host} -H 'User-Agent: '${random_useragent}'')
            if [ $? -eq 0 ]; then
                site_title=$(echo ${checksrc} | grep -oE '<title>(.*)</title>' | sed -e 's/<title>//' -e 's/<\/title>//')
                echo "${host} online | ${site_title}"
            else
                echo "${host} offline"
            fi
        else
            echo "${host}"
        fi
    fi
done <<< "${hosts}"
#rm assets/tmp/sources.*
