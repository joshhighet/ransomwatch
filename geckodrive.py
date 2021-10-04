#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
loads the dom and fetches html source after javascript rendering w/ firefox, geckodriver & selenium
use sharedutils.py:socksfetcher for faster results if no post-processing required
'''
import time
import requests
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import WebDriverException

from sharedutils import checktcp
from sharedutils import randomagent

from sharedutils import sockshost, socksport

from sharedutils import stdlog, dbglog, errlog, honk

requests.packages.urllib3.disable_warnings()

def main(webpage):
    '''
    main function to fetch webpages with javascript rendering supporting onion routing
    '''
    stdlog('geckodriver: ' + 'starting to fetch ' + webpage)
    dbglog('geckodriver: ' + 'configuring options, user agent & cert preacceptance')
    options = Options()
    options.headless = True
    options.add_argument("start-maximized")
    profile = webdriver.FirefoxProfile()
    profile.accept_untrusted_certs = True
    profile.set_preference("general.useragent.override", randomagent())
    if '.onion' in webpage:
        stdlog('geckodriver: ' + 'appears we are dealing with an onionsite')
        if not checktcp(sockshost, socksport):
            honk('geckodriver: ' + 'socks proxy not available and required for onionsites!')
        else:
            stdlog(
                'geckodriver: ' + 'assumed torsocks proxy found - tcp://' \
                + sockshost + ':' + str(socksport)
            )
            stdlog('geckodriver: ' + 'configuring proxy settings')
            profile.set_preference('network.proxy.type', 1)
            profile.set_preference('network.proxy.socks', sockshost)
            profile.set_preference('network.proxy.socks_port', int(socksport))
            profile.set_preference("network.proxy.socks_remote_dns", True)
    try:
        stdlog('geckodriver: ' + 'starting webdriver')
        driver = webdriver.Firefox(options=options, firefox_profile=profile, timeout=30)
        stdlog('geckodriver: ' + 'fetching webpage')
        driver.get(webpage)
        # set the number of seconds to wait before working with the DOM
        sleeptz = 5
        stdlog('geckodriver: ' + 'waiting ' + str(sleeptz) + ' seconds to render elements')
        time.sleep(sleeptz)
        if 'lockbitapt' in webpage:
            stdlog('geckodriver: ' + 'special detected, waiting for captcha')
            driver.add_cookie({"name": "ddosproteck", "value": "lol"})
            driver.find_element_by_css_selector('button').click()
        '''
        get html from dom after js processing and page rendering complete
        '''
        source = driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
        stdlog('geckodriver: ' + 'fetched')
    except WebDriverException as e:
        errlog('geckodriver: ' + 'error: ' + str(e))
        driver.quit()
        stdlog('geckodriver: ' + 'webdriver quit')
        return None
    if driver:
        driver.quit()
        stdlog('geckodriver: ' + 'webdriver quit')
    return source
