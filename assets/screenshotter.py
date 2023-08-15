#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import requests
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError, Error as PlaywrightError

def setup_browser(play):
    browser = play.chromium.launch(proxy={"server": "socks5://127.0.0.1:9050"}, args=[''])
    return browser

def screenshot(browser, webpage, fqdn):
    print('webshot: {}'.format(webpage))
    context = None
    try:
        context = browser.new_context(ignore_https_errors=True)
        page = context.new_page()
        page.goto(webpage, wait_until='load', timeout=120000)
        page.bring_to_front()
        page.wait_for_timeout(15000)
        page.mouse.move(x=500, y=400)
        page.wait_for_load_state('networkidle')
        page.mouse.wheel(delta_y=2000, delta_x=0)
        page.wait_for_load_state('networkidle')
        page.wait_for_timeout(5000)
        name = 'source/screenshots/' + fqdn.replace('.', '-') + '.png'
        page.screenshot(path=name, full_page=True)
    except (PlaywrightTimeoutError, PlaywrightError) as e:
        print(f'Error with {webpage}: {e}')
    finally:
        if context:
            context.close()

def main():
    if not os.path.exists('source/screenshots/'):
        os.makedirs('source/screenshots/')
    groups = requests.get('https://ransomwhat.telemetry.ltd/groups').json()
    with sync_playwright() as play:
        browser = setup_browser(play)
        for group in groups:
            print('group: {}'.format(group['name']))
            for webpage in group['locations']:
                if webpage['available'] is True:
                    screenshot(browser, webpage['slug'], webpage['fqdn'])
                else:
                    print(webpage['slug'] + ' not available')
        browser.close()

if __name__ == '__main__':
    main()