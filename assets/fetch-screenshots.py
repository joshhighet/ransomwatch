'''
screenshot up hosts using selenium w/firefox webdriver
'''
import logging
import requests
from threading import Thread
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.firefox.options import Options

from sharedutils import sockshost, socksport
from sharedutils import stdlog, dbglog, errlog, honk
from sharedutils import checktcp, openjson, randomagent

logging.basicConfig(level=logging.INFO)
requests.packages.urllib3.disable_warnings()

def main(webpage):
    stdlog('webshot: {}'.format(webpage))
    if not checktcp(sockshost, socksport):
        honk("socks proxy not available and required for scraping!")
    options = Options()
    options.headless = True
    options.accept_untrusted_certs = True
    options.add_argument("start-maximized")
    options.set_preference('network.http.timeout', 20000)
    options.set_preference('dom.max_script_run_time', 15)
    options.set_preference('layout.css.devPixelsPerPx','2.0')
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
        stdlog('webshot: {}'.format(webpage) + ' starting browser')
        driver = webdriver.Firefox(options=options)
        driver.set_page_load_timeout(60)
        driver.set_window_size(2560, 1600)
        driver.get(webpage)
        driver.implicitly_wait(10)
        logging.info('webshot: {}'.format(webpage) + ' taking screenshot')
        screenshot = driver.get_screenshot_as_png()
        driver.quit()
    except WebDriverException as wde:
        if 'dnsNotFound' in wde.msg:
            errlog('webshot: {}'.format(webpage) + ' dnsNotFound')
            return
        elif 'connectionFailure' in wde.msg:
            errlog('webshot: {}'.format(webpage) + ' connection refused')
            return
        errlog('webshot: {}'.format(webpage) + ' webdriver error: {}'.format(wde))
        return
    return screenshot

def threadsafe(slug, fqdn):
    screenshot = main(slug)
    if screenshot:
        outfile = 'screenshots/' + fqdn.replace('.', '-') + '.png'
        with open(outfile, 'wb') as f:
            f.write(screenshot)


groups = openjson('groups.json')
for group in groups:
    for webpage in group['locations']:
        if webpage['available'] == True:    
            t = Thread(target=threadsafe, args=(webpage['slug'], webpage['fqdn']))
            t.start()
