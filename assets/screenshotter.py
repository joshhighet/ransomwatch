#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import requests
import argparse
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError, Error as PlaywrightError

def setup_browser(play):
    browser = play.chromium.launch(proxy={"server": "socks5://127.0.0.1:9050"}, args=[''])
    return browser

def screenshot(browser, webpage, fqdn):
    print('screenshotting: {}'.format(webpage))
    context = None
    try:
        context = browser.new_context(ignore_https_errors=True)
        page = context.new_page()
        page.goto(webpage, wait_until='load', timeout=15000)
        page.bring_to_front()
        page.wait_for_timeout(15000)
        page.mouse.move(x=500, y=400)
        page.wait_for_load_state('networkidle')
        page.mouse.wheel(delta_y=2000, delta_x=0)
        page.wait_for_load_state('networkidle')
        page.wait_for_timeout(5000)
        name = 'source/screenshots/' + fqdn.replace('.', '-') + '.png'
        page.screenshot(path=name, full_page=True)
        print(f'screenshot saved to: {name}')
    except (PlaywrightTimeoutError, PlaywrightError) as e:
        print(f'error with {webpage}: {e}')
    finally:
        if context:
            context.close()

def screenshot_single_url(browser, url):
    domain = url.split("//")[-1].split("/")[0]
    screenshot(browser, url, domain)

def main():
    parser = argparse.ArgumentParser(description='ransomwatchshot.')
    parser.add_argument('--url', help='screenshot a given URL')
    parser.add_argument('--all', action='store_true', help='screenshot all online ransomwatch URLs into source/screenshots/')
    parser.add_argument('--stdin', action='store_true', help='screenshot a URL provided from stdin')
    args = parser.parse_args()
    if not args.url and not args.all and not args.stdin:
        parser.print_help()
        return
    if not os.path.exists('source/screenshots/'):
        os.makedirs('source/screenshots/')
    with sync_playwright() as play:
        browser = setup_browser(play)
        if args.stdin:
            for line in sys.stdin:
                url = line.strip()
                if url:
                    screenshot_single_url(browser, url)
        elif args.url:
            screenshot_single_url(browser, args.url)
        elif args.all:
            groups = requests.get('https://ransomwhat.telemetry.ltd/groups').json()
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
