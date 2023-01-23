import os
import json
import requests

if os.path.exists('groups.json'):
    groups = json.load(open('groups.json'))
else:
    groups = requests.get('https://ransomwhat.telemetry.ltd/groups').json()
eventdict = []
for group in groups:
    for loc in group['locations']:
        event = group.copy()
        event.pop('locations')
        event.update(loc)
        eventdict.append(event)

with open('assets/groups-kv.json', 'w') as f:
    json.dump(eventdict, indent=2, fp=f)
