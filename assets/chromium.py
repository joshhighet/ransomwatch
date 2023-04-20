#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
loads the dom and fetches html source after javascript rendering w/ chrome/selenium
use sharedutils.py:socksfetcher for faster results if no post-processing required
'''
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException

from sharedutils import checktcp
from sharedutils import randomagent

from sharedutils import sockshost, socksport

from sharedutils import stdlog, dbglog, errlog, honk

requests.packages.urllib3.disable_warnings()

def main(webpage):
    '''
    secondary function to fetch webpages with javascript (ref geckodriver) - rendering supporting onion routing, backup
    '''
    stdlog('chromium: ' + 'starting to fetch ' + webpage)
    dbglog('chromium: ' + 'configuring options, user agent & cert preacceptance')
    options = Options()
    options.headless = True
    options.add_argument("start-maximized")
    options.accept_untrusted_certs = True
    options.add_argument('user-agent=' + randomagent())
    if '.onion' in webpage:
        stdlog('chromium: ' + 'appears we are dealing with an onionsite')
        if not checktcp(sockshost, socksport):
            honk('chromium: ' + 'socks proxy not available and required for onionsites!')
        else:
            stdlog(
                'chromium: ' + 'assumed torsocks proxy found - tcp://' \
                + sockshost + ':' + str(socksport)
            )
            stdlog('chromium: ' + 'configuring proxy settings')
            options.add_argument('--proxy-server=socks5://' + sockshost + ':' + str(socksport))
    try:
        stdlog('chromium: ' + 'starting webdriver')
        driver = webdriver.Chrome(options=options)
        driver.set_page_load_timeout(30)
        stdlog('chromium: ' + 'fetching webpage')
        driver.get(webpage)
        sleeptz = 5
        if 'lockbitapt' in webpage:
            stdlog('chromium: ' + 'appears to be a lockbit site, giving extra loadtime')
            time.sleep(20)
        stdlog('chromium: ' + 'waiting ' + str(sleeptz) + ' seconds to render elements')
        time.sleep(sleeptz)
        source = driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
        stdlog('chromium: ' + 'fetched')
    except WebDriverException as e:
        if 'net::ERR_SOCKS_CONNECTION_FAILED' in str(e):
            errlog('chromium: ' + 'socks request unable to route to host, check hsdir resolution status!')
        elif 'Timed out receiving message from renderer:' in str(e):
            errlog('chromium: ' + 'rendering timed out, took 2 long')
        else:
            errlog('chromium: ' + 'unhandled error: ' + str(e))
            exit()
        try:
            driver.quit()
            stdlog('chromium: ' + 'webdriver quit')
        except UnboundLocalError:
            pass
        return None
    if driver:
        driver.quit()
        stdlog('chromium: ' + 'webdriver quit')
    return source
