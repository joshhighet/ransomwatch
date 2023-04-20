#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
screenshot available hosts using playwright

// setup
$ pip3 install playwright
$ playwright install
'''

import os
import requests
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from sharedutils import sockshost, socksport
from sharedutils import stdlog, errlog, honk
from sharedutils import openjson        

def screenshot(webpage,fqdn):
    stdlog('webshot: {}'.format(webpage))
    with sync_playwright() as play:
        try:
            browser = play.chromium.launch(proxy={"server": "socks5://127.0.0.1:9050"},
                args=[''])
            context = browser.new_context(ignore_https_errors= True )
            page = context.new_page()
            page.goto(webpage, wait_until='load', timeout = 120000)
            page.bring_to_front()
            delay=15000
            page.wait_for_timeout(delay)
            page.mouse.move(x=500, y=400)
            page.wait_for_load_state('networkidle')
            page.mouse.wheel(delta_y=2000, delta_x=0)
            page.wait_for_load_state('networkidle')
            page.wait_for_timeout(5000)
            name = 'docs/screenshots/' + fqdn.replace('.', '-') + '.png'
            page.screenshot(path=name, full_page=True)
        except PlaywrightTimeoutError:
            stdlog('Timeout!')
        browser.close()

def main():
    groups = openjson('groups.json')
    for group in groups:
        stdlog('group: {}'.format(group['name']))
        for webpage in group['locations']:
            if webpage['available'] is True:
                screenshot(webpage['slug'],webpage['fqdn'])
            else:
                stdlog('webshot: {}'.format(webpage['slug']) + ' not available')

if __name__ == '__main__':
    main()
