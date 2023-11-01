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
    stdlog('geckodriver: ' + 'starting to fetch ' + webpage)
    dbglog('geckodriver: ' + 'configuring options, user agent & cert preacceptance')
    options = Options()
    options.add_argument("-headless") 
    options.set_preference('dom.max_script_run_time', 20)
    options.accept_untrusted_certs = True
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
        driver.set_page_load_timeout(20)
        stdlog('geckodriver: ' + 'fetching webpage')
        start_time = time.time()
        try:
            driver.get(webpage)
        except WebDriverException as e:
            if 'about:neterror?e=dnsNotFound' in str(e):
                errlog('geckodriver: ' + 'socks request unable to route to host, check hsdir resolution status!')
            elif 'about:neterror?e=netTimeout' in str(e):
                errlog('geckodriver: ' + 'socks request timed out!')
            elif "Navigation timed out after" in str(e):
                errlog('geckodriver: ' + 'pageload timeout reached!')
            else:
                errlog('geckodriver: ' + 'unknown error during page load: ' + str(e))
            driver.quit()
            return None
        sleeptz = 5
        if 'lockbitapt' in webpage:
            time.sleep(7)
            driver.implicitly_wait(3)
            # driver.add_cookie({"name": "ddosproteck", "value": "lol"})
            # driver.find_element_by_css_selector('button').click()
        stdlog('geckodriver: ' + 'waiting ' + str(sleeptz) + ' seconds to render elements')
        time.sleep(sleeptz)
        '''
        get html from dom after js processing and page rendering complete
        '''
        source = driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
        end_time = time.time()
        elapsed_time = end_time - start_time
        stdlog('geckodriver: ' + f'action {webpage} took {elapsed_time:.2f} seconds')
    except WebDriverException as e:
        errlog('geckodriver: ' + 'error: ' + str(e))
        driver.quit()
        return None
    finally:
        if driver:
            driver.quit()
            stdlog('geckodriver: ' + 'webdriver quit')
    return source
