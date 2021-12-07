import os
import json
import logging
from bs4 import BeautifulSoup
from sharedutils import stdlog, dbglog, errlog, honk

for file in os.listdir('source'):
    if file.endswith('.html'):
        stdlog('processing file: ' + file)
        with open('source/' + file, 'r') as f:
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
                logging.debug('link: {}'.format(link))
                if link.get('href'):
                    if link.get('href').startswith('http'):
                        logging.debug('external url: {}'.format(link.get('href')))
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
                            pass
                        elif link.get('href').startswith('javascript'):
                            unhandled.append(link.get('href'))
                            pass
                        elif link.get('href') == '/':
                            unhandled.append(link.get('href'))
                            pass
                        elif link.get('href').startswith('/'):
                            link = fqdn + str(link.get('href') )
                            urls.append(link)
                        else:
                            unhandled.append(link.get('href'))
            infosheet['urls'] = list(set(urls))
            infosheet['externalurls'] = list(set(externalurls))
            infosheet['emails'] = list(set(emails))
            infosheet['phnumbers'] = list(set(phnum))
            infosheet['unhandled'] = list(set(unhandled))
            infosheet['source'] = 'ransomwatch/source/' + file
            with open('source/linkanalysis/' + fqdn + '.json', 'w') as f:
                json.dump(infosheet, f, indent=4)
            stdlog('created findings file: ' + 'source/linkanalysis/' + fqdn + '.json')
