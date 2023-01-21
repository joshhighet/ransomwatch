#!/bin/bash

# get groups with parsers enabled
# jq -r '.[] | select(.parser==true) | .name' groups.json

# get groups with captcha
# jq -r '.[] | select(.captcha==true) | .name' groups.json

if [ "${1}" == "-h" ]; then
    echo "by default - will run very basic checks on each parser and report on those not returning anything"
    echo "switch: print all parsers | -p"
    echo "switch: print specific group | -p <groupname>"
    exit 0
fi

shell_parsers=`grep -A 2 "parser = '''" parsers.py | sed -e "/parser = '''/d" -e "/'''/d" -e '/^--$/d'`
shell_parsers_total=`echo "${shell_parsers}" | wc -l | sed -e 's/^[ \t]*//'`

echo "checking each parser is returning results (line-delim posts)"
echo

if [ "${1}" == "-p" ] && [ "${2}" != "" ]; then
    while read -r line; do
        if [[ ${line} =~ %s ]]; then
            line=${line//%s/grep -oE}
        fi
        if [[ ${line} =~ ${2} ]]; then
            echo ${line}
        fi
    done <<< "${shell_parsers}"
    exit 0
fi

if [ "${1}" == "-p" ]; then
    while read -r line; do
        if [[ ${line} =~ %s ]]; then
            line=${line//%s/grep -oE}
        fi
        echo ${line}
    done <<< "${shell_parsers}"
    exit 0
fi

brokecount=0
while read -r line; do
    if [[ ${line} =~ %s ]]; then
        line=${line//%s/grep -oE}
    fi
    results=`echo "${line}" | bash`
    if [ -z "${results}" ]; then
        echo "${line}"
        brokecount=$((brokecount+1))
        shell64=`echo "${line}" | base64`
        echo "debug64: ${shell64}"
        echo
    fi
done <<< "$shell_parsers"

echo
echo "returning nothing: ${brokecount}"
echo "total parsers: ${shell_parsers_total}"
