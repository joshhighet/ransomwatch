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
    options.set_preference('dom.max_script_run_time', 15)
    options.add_argument("start-maximized")
    options.accept_untrusted_certs = True
    options.set_preference('network.http.timeout', 20000)
    options.set_preference("general.useragent.override", randomagent())
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
            options.set_preference('network.proxy.type', 1)
            options.set_preference('network.proxy.socks', sockshost)
            options.set_preference('network.proxy.socks_port', int(socksport))
            options.set_preference("network.proxy.socks_remote_dns", True)
    try:
        stdlog('geckodriver: ' + 'starting webdriver')
        driver = webdriver.Firefox(options=options)
        stdlog('geckodriver: ' + 'fetching webpage')
        driver.get(webpage)
        # set the number of seconds to wait before working with the DOM
        sleeptz = 5
        if 'lockbitapt3' in webpage:
            time.sleep(20)
            #driver.implicitly_wait(20)
        stdlog('geckodriver: ' + 'waiting ' + str(sleeptz) + ' seconds to render elements')
        time.sleep(sleeptz)
        #if 'lockbitapt' in webpage:
        #    stdlog('geckodriver: ' + 'special detected, waiting for captcha')
        #    driver.add_cookie({"name": "ddosproteck", "value": "lol"})
        #    driver.find_element_by_css_selector('button').click()
        '''
        get html from dom after js processing and page rendering complete
        '''
        source = driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
        stdlog('geckodriver: ' + 'fetched')
    except WebDriverException as e:
        # if e contains neterror?e=dnsNotFound, then we are dealing with an onion site failing hsdir
        if 'about:neterror?e=dnsNotFound' in str(e):
            errlog('geckodriver: ' + 'socks request unable to route to host, check hsdir resolution status!')
        elif 'about:neterror?e=netTimeout' in str(e):
            errlog('geckodriver: ' + 'socks request timed out!')
        else:
            errlog('geckodriver: ' + 'error: ' + str(e))
        try:
            driver.quit()
            stdlog('geckodriver: ' + 'webdriver quit')
        except UnboundLocalError:
            pass
        return None
    if driver:
        driver.quit()
        stdlog('geckodriver: ' + 'webdriver quit')
    return source
