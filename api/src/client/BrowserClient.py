import time
from python_helper import Constant as c
from python_helper import ObjectHelper, log, StringHelper
from python_framework import SimpleClient, SimpleClientMethod

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys

from bs4 import BeautifulSoup

DEFAULT_WEBDRIVER_LARGE_TIMEOUT = 1
DEFAULT_WEBDRIVER_TIMEOUT = DEFAULT_WEBDRIVER_LARGE_TIMEOUT * .2
DEFAULT_WEBDRIVER_TIMEOUT_FRACTION = DEFAULT_WEBDRIVER_TIMEOUT / 50

DEFAULT_BOWSER_CLASS = webdriver.Chrome

@SimpleClient()
class BrowserClient:

    @SimpleClientMethod()
    def getBrowserOptions(self, anonymous=False, deteach=True) :
        chromeOptions = webdriver.ChromeOptions()
        if anonymous :
            chromeOptions.add_argument("--incognito")
        if deteach :
            chromeOptions.add_experimental_option("detach", True)
        return chromeOptions

    @SimpleClientMethod()
    def getNewBrowser(self, options=None) :
        options = options if ObjectHelper.isNotNone(options) else self.getBrowserOptions()
        browser = DEFAULT_BOWSER_CLASS(ChromeDriverManager().install(), chrome_options=options)
        log.debug(self.getNewBrowser, f'session_id: {browser.session_id}')
        log.debug(self.getNewBrowser, f'command_executor: {browser.command_executor._url}')
        return browser

    @SimpleClientMethod()
    def getNewAnonymousBrowser(self) :
        return self.getNewBrowser(options=self.getBrowserOptions(anonymous=True))

    @SimpleClientMethod(requestClass=[str, DEFAULT_BOWSER_CLASS])
    def accessUrl(self, url, browser) :
        try :
            browser.get(url)
            time.sleep(DEFAULT_WEBDRIVER_TIMEOUT)
        except :
            browser.get(url)
            time.sleep(DEFAULT_WEBDRIVER_LARGE_TIMEOUT)
        return browser

    @SimpleClientMethod(requestClass=[str])
    def openInNewBrowser(self, url) :
        if ObjectHelper.isNotNone(url) :
            browser = self.getNewBrowser()
            return self.accessUrl(url, browser)

    @SimpleClientMethod(requestClass=[str])
    def openInNewAnonymousBrowser(self, url) :
        if ObjectHelper.isNotNone(url) :
            browser = self.getNewAnonymousBrowser()
            return self.accessUrl(url, browser)

    @SimpleClientMethod(requestClass=[str, DEFAULT_BOWSER_CLASS])
    def openInNewTab(self, url, browser):
        if ObjectHelper.isNotNone(url) :
            self.newTab(browser)
            return self.accessUrl(url, browser)

    @SimpleClientMethod(requestClass=[DEFAULT_BOWSER_CLASS])
    def newTab(self, browser) :
        browser.execute_script("window.open();")
        time.sleep(DEFAULT_WEBDRIVER_TIMEOUT)
        browser.switch_to.window(browser.window_handles[-1])
        time.sleep(DEFAULT_WEBDRIVER_TIMEOUT_FRACTION)

    @SimpleClientMethod(requestClass=[str])
    def typeIn(self, text, element=None) :
        element.send_keys(Keys.CONTROL, 'a')
        element.send_keys(text)

    @SimpleClientMethod(requestClass=[str])
    def typeInAndHitEnter(self, text, element=None) :
        self.typeIn(text, element=element)
        element.send_keys(Keys.ENTER)
        time.sleep(DEFAULT_WEBDRIVER_TIMEOUT_FRACTION)

    @SimpleClientMethod(requestClass=[str, DEFAULT_BOWSER_CLASS])
    def getAttribute(self, attributeName, element) :
        return element.get_attribute(attributeName)

    @SimpleClientMethod(requestClass=[str, DEFAULT_BOWSER_CLASS])
    def findByXPath(self, xPath, browser) :
        element = browser.find_element_by_xpath(xPath)
        time.sleep(DEFAULT_WEBDRIVER_TIMEOUT_FRACTION)
        return element

    @SimpleClientMethod(requestClass=[str, DEFAULT_BOWSER_CLASS])
    def findAllByXPath(self, xPath, browser) :
        elementList = browser.find_elements_by_xpath(xPath)
        time.sleep(DEFAULT_WEBDRIVER_TIMEOUT_FRACTION)
        return elementList

    @SimpleClientMethod(requestClass=[str, DEFAULT_BOWSER_CLASS])
    def accessByXPath(self, xPath, browser) :
        element = self.findByXPath(xPath, browser)
        self.access(element)

    @SimpleClientMethod(requestClass=[DEFAULT_BOWSER_CLASS])
    def access(self, element) :
        element.click()
        time.sleep(DEFAULT_WEBDRIVER_TIMEOUT)
        return element

    @SimpleClientMethod(requestClass=[str, DEFAULT_BOWSER_CLASS])
    def findByClass(self, className, browser) :
        if c.SPACE in className :
            return self.findByCss(StringHelper.join([c.NOTHING, *className.split()], character=c.DOT), browser)
        element = browser.find_element_by_class_name(className)
        time.sleep(DEFAULT_WEBDRIVER_TIMEOUT_FRACTION)
        return element

    @SimpleClientMethod(requestClass=[str, DEFAULT_BOWSER_CLASS])
    def findByCss(self, css, browser) :
        element = browser.find_element_by_css_selector(css)
        time.sleep(DEFAULT_WEBDRIVER_TIMEOUT_FRACTION)
        return element

    @SimpleClientMethod(requestClass=[str, DEFAULT_BOWSER_CLASS])
    def findByPartialClass(self, partialClass, browser, html=None) :
        elementList = self.findAllClassByPartialClass(partialClass, browser, html=html)
        if 1 <= len(elementList) :
            return elementList[0]

    @SimpleClientMethod(requestClass=[str, DEFAULT_BOWSER_CLASS])
    def findAllClassByPartialClass(self, partialClass, browser, html=None) :
        # print(f'partialClass: {partialClass}')
        # print(browser.get_attribute('innerHTML'))
        soup = BeautifulSoup(html if ObjectHelper.isNotNone(html) else self.getAttribute('innerHTML', browser), 'html.parser')
        # print(soup.prettify())
        soupElementList = soup.find_all('span', attrs={'class': lambda e: partialClass in e if e else False})
        # print(f'soupElementList: {soupElementList}')
        # from python_helper import ReflectionHelper
        # for soupElement in soupElementList :
        #     print(f'type({soupElement.span}): {type(soupElement.span)}')
            # log.prettyPython(self.findAllClassByPartialClass, 'soupElement', ReflectionHelper.getItNaked(soupElement), logLevel=log.DEBUG)
            # print(soupElement.__dict__)
        # return [self.findByClass(str(StringHelper.join(soupElement.attrs['class'], character=c.SPACE)), browser) for soupElement in soupElementList]
        return [self.findByClass(str(StringHelper.join(soupElement.attrs['class'], character=c.SPACE)), browser) for soupElement in soupElementList]

    @SimpleClientMethod(requestClass=[DEFAULT_BOWSER_CLASS])
    def acceptAlert(self, browser):
        alert = browser.switch_to.alert
        alert.accept()
        time.sleep(DEFAULT_WEBDRIVER_TIMEOUT)

    @SimpleClientMethod(requestClass=[DEFAULT_BOWSER_CLASS])
    def maximize(self, browser) :
        browser.maximize_window()

    @SimpleClientMethod(requestClass=[DEFAULT_BOWSER_CLASS])
    def close(self, browser) :
        try :
            browser.close()
        except Exception as exception :
            log.error(self.close, 'Not possible to close browser properly', exception)

    @SimpleClientMethod(requestClass=[str, str])
    def retrieveBrowserSession(self, session_id, executor_url):
        '''
        ###############################################################
        retrieverBrowser = create_driver_session(command_executor=executor_url, desired_capabilities={})
        ###############################################################

        driver = webdriver.Firefox()
        executor_url = driver.command_executor._url
        session_id = driver.session_id
        driver.get("https://www.google.com")
        print(session_id)
        print(executor_url)
        driver2 = create_driver_session(session_id, executor_url)
        print(driver2.current_url)
        '''
        from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver

        # Save the original function, so we can revert our patch
        org_command_execute = RemoteWebDriver.execute

        def new_command_execute(self, command, params=None):
            if command == "newSession":
                # Mock the response
                return {'success': 0, 'value': None, 'sessionId': session_id}
            else:
                return org_command_execute(self, command, params)

        # Patch the function before creating the driver object
        RemoteWebDriver.execute = new_command_execute

        new_driver = webdriver.Remote(command_executor=executor_url, desired_capabilities={})
        new_driver.session_id = session_id

        # Replace the patched function with original function
        RemoteWebDriver.execute = org_command_execute

        return new_driver

################################################################################
# low level

# from io import StringIO
# from selenium import webdriver
# import lxml.etree
# import lxml.html
# parser = lxml.etree.HTMLParser()
# # html = self.browser.execute_script("return document.documentElement.outerHTML")
# # tree = lxml.etree.parse(StringIO(html), parser)
# # print(tree)
# # print(lxml.html.tostring(tree))
# tree = lxml.etree.parse(StringIO(browser.get_attribute('innerHTML')), parser)
