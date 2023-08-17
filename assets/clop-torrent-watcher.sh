#!/bin/bash
# you will need to run the torrent-metadata server somewhere accessible from this runtime
# in this case, torrent-metadata.dark is my local torrent-metadata instance
# https://github.com/schardev/torrent-metadata

# to retrieve the desired metadata such as the file names you hasve to briefly commence seeding
# for this reason you should avoid running the torrent metadata server on your own networks

fetchfile='clop-toznnag5o3ambca56s2yacteu7q7x2avrfherzmz4nmujrjuib4iusad.html'
curl -s https://raw.githubusercontent.com/joshhighet/ransomwatch/main/source/${fetchfile} | \
awk -F'"' '
/<td><a href="http:/ {title=$2}
/<a href="magnet:/ {
    magnet=$2;
    print title " - " magnet;
    system("curl -s torrent-metadata.dark:3000 -H \"Content-Type: application/json\" -d \047{\"query\": \"" magnet "\"}\047 | jq ."); 
}
'
