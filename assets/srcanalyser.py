#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import json
import logging
from bs4 import BeautifulSoup

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

if not os.path.exists('source/linkanalysis'):
    os.makedirs('source/linkanalysis')

def display_output(infosheet, file_name):
    print("\nprocessing file:", file_name)
    print("="*40)
    for key, value in infosheet.items():
        if value:
            print("\n", key.upper())
            print("-"*30)
            if isinstance(value, list):
                for item in value:
                    print(item)
            else:
                print(value)
    print("\n" + "="*40 + "\n")

for file in os.listdir('source'):
    if file.endswith('.html'):
        logging.info('processing file: ' + file)
        with open('source/' + file, 'r', encoding='utf-8') as f:
            fqdn = file.split('-')[1].strip('.html')
            infosheet = {
                'urls': list(),
                'externalurls': list(),
                'emails': list(),
                'phnumbers': list(),
                'unhandled': list(),
                'meta': None
            }
            soup = BeautifulSoup(f.read(), 'html.parser')
            urls = []
            emails = []
            phnum = []
            unhandled = []
            externalurls = []
            for link in soup.find_all('a'):
                if link.get('href'):
                    if link.get('href').startswith('http'):
                        if fqdn not in link.get('href'):
                            externalurls.append(link.get('href'))
                        else:
                            urls.append(link.get('href'))
                    elif link.get('href').startswith('tel:'):
                        phnum.append(link.get('href').strip('tel:'))
                    elif link.get('href').startswith(('mailto', 'mailTo')):
                        emails.append(link.get('href').strip('mailTo: '))
                    else:
                        if link.get('href').startswith('#'):
                            unhandled.append(link.get('href'))
                        elif link.get('href').startswith('javascript'):
                            unhandled.append(link.get('href'))
                        elif link.get('href') == '/':
                            unhandled.append(link.get('href'))
                        elif link.get('href').startswith('/'):
                            urls.append(fqdn + str(link.get('href')))
                        else:
                            unhandled.append(link.get('href'))
            infosheet['urls'] = list(set(urls))
            infosheet['externalurls'] = list(set(externalurls))
            infosheet['emails'] = list(set(emails))
            infosheet['phnumbers'] = list(set(phnum))
            infosheet['unhandled'] = list(set(unhandled))
            infosheet['source'] = 'ransomwatch/source/' + file
            display_output(infosheet, file)
            with open('source/linkanalysis/' + fqdn + '.json', 'w', encoding='utf-8') as f:
                json.dump(infosheet, f, indent=4)
            logging.info('created findings file: ' + 'source/linkanalysis/' + fqdn + '.json')
