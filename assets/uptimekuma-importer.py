# uptime-kuma is a free and open source uptime monitor
# https://github.com/louislam/uptime-kuma

# this script converts the ransomwatch group dictionary into an uptime-kuma importable json file
# whilst you can not bulk import hosts into uptime-kuma - you can export a backup, then reimport
# use this script to generate the "backup file" and import it

# note;
# you should change startidnum to the next available id number in your uptime-kuma instance
# if you have existing hosts in an uptime-kuma deployment you should add them into the generated file otherwise they will be overwritten
# the notificationIDList is dependent on your notification settings in uptime-kuma - you can set this to a raft of services
# the proxyId is dependent on your proxy settings in uptime-kuma (you will need a socks5 proxy configured and accessible to reach onionsites!)

import os
import json
import requests

startidnum = 1

def genschema(idnumber, name, domain):
    return {
        "id": idnumber,
        "name": name,
        "url": domain,
        "method": "GET",
        "hostname": None,
        "port": None,
        "maxretries": 0,
        "weight": 2000,
        "active": 1,
        "type": "http",
        "interval": 60,
        "retryInterval": 60,
        "resendInterval": 0,
        "keyword": None,
        "expiryNotification": False,
        "ignoreTls": False,
        "upsideDown": False,
        "maxredirects": 10,
        "accepted_statuscodes": [
            "200-299"
        ],
        "dns_resolve_type": "A",
        "dns_resolve_server": "1.1.1.1",
        "dns_last_result": None,
        "docker_container": "",
        "docker_host": None,
        "proxyId": 1,
        "notificationIDList": {
            "1": True
        },
        "tags": [
            {
                "id": 2,
                "monitor_id": 1,
                "tag_id": 1,
                "value": "",
                "name": "ransomwatch",
                "color": "#DB2777"
            }
        ],
        "maintenance": False,
        "mqttTopic": "",
        "mqttSuccessMessage": "",
        "databaseQuery": None,
        "authMethod": None,
        "grpcUrl": None,
        "grpcProtobuf": None,
        "grpcMethod": None,
        "grpcServiceName": None,
        "grpcEnableTls": False,
        "radiusCalledStationId": None,
        "radiusCallingStationId": None,
        "headers": None,
        "body": None,
        "grpcBody": None,
        "grpcMetadata": None,
        "basic_auth_user": None,
        "basic_auth_pass": None,
        "pushToken": None,
        "databaseConnectionString": None,
        "radiusUsername": None,
        "radiusPassword": None,
        "radiusSecret": None,
        "mqttUsername": "",
        "mqttPassword": "",
        "authWorkstation": None,
        "authDomain": None,
        "includeSensitiveData": True
    }

groupdata = requests.get("https://ransomwhat.telemetry.ltd/groups").json()
array_to_create = {}
output = []
for group in groupdata:
    if len(group['locations']) > 1:
        i = 0
        for location in group['locations']:
            i += 1
            array_to_create[group['name'] + "-" + str(i)] = location['slug']
    else:
        array_to_create[group['name']] = group['locations'][0]['slug']

for name, domain in array_to_create.items():
    output.append(genschema(startidnum, name, domain))
    startidnum += 1
    
print(json.dumps(output, indent=4))
