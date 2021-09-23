import time
from python_helper import Constant as c
from python_helper import ObjectHelper, log, StringHelper
from python_framework import SimpleClient, SimpleClientMethod
from python_framework import WebBrowser as PythonFrameworkWebBrowser

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys

from bs4 import BeautifulSoup

import KeyboardUtil
from domain import BrowserConstants

from io import BytesIO
import win32clipboard
from PIL import Image

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'

@SimpleClient()
class BrowserClient:

    @SimpleClientMethod()
    def getBrowserOptions(self, anonymous=False, deteach=True) :
        chromeOptions = webdriver.ChromeOptions()

        chromeOptions.add_argument('--ignore-certificate-errors')
        chromeOptions.add_argument(f'user-agent={USER_AGENT}')
        # chromeOptions.add_argument('--disable-blink-features=AutomationControlled')
        # chromeOptions.add_experimental_option("excludeSwitches", ["enable-automation"])
        # chromeOptions.add_experimental_option('useAutomationExtension', False)
        # chromeOptions.add_argument('--disable-extensions')
        # chromeOptions.add_argument('--disable-gpu')
        # chromeOptions.add_argument('--disable-dev-shm-usage')
        # chromeOptions.add_argument('--no-sandbox')
        # chromeOptions.add_argument("headless")
        # chromeOptions.add_argument('--incognito')
        # chromeOptions.add_experimental_option('detach', True)

        # chromeOptions.add_argument('--ignore-certificate-errors')
        # chromeOptions.add_argument(f'user-agent={USER_AGENT}')
        # chromeOptions.add_argument('--disable-blink-features=AutomationControlled')
        # chromeOptions.add_experimental_option("excludeSwitches", ["enable-automation"])
        # chromeOptions.add_experimental_option('useAutomationExtension', False)
        # # chromeOptions.add_argument('--disable-software-rasterizer')
        # chromeOptions.add_argument('--disable-extensions')
        # # chromeOptions.add_argument('--disable-gpu')
        # chromeOptions.add_argument('--disable-dev-shm-usage')
        # chromeOptions.add_argument('--no-sandbox')
        # chromeOptions.add_argument("headless")
        if anonymous :
            chromeOptions.add_argument('--incognito')
        if deteach :
            chromeOptions.add_experimental_option('detach', True)
        return chromeOptions

    @SimpleClientMethod()
    def getNewBrowser(self, options=None, hidden=False) :
        options = options if ObjectHelper.isNotNone(options) else self.getBrowserOptions()
        browser = BrowserConstants.BOWSER_CLASS(ChromeDriverManager().install(), chrome_options=options)
        browser.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": f'{USER_AGENT}'})

        browser.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        log.debug(self.getNewBrowser, f'session_id: {browser.session_id}')
        log.debug(self.getNewBrowser, f'command_executor: {browser.command_executor._url}')
        return browser

    @SimpleClientMethod()
    def getNewAnonymousBrowser(self) :
        return self.getNewBrowser(options=self.getBrowserOptions(anonymous=True))

    @SimpleClientMethod(requestClass=[str, BrowserConstants.BOWSER_CLASS])
    def accessUrl(self, url, browser) :
        parsedUrl = PythonFrameworkWebBrowser.getParsedUrl(url, host='localhost')
        try :
            browser.get(parsedUrl)
            time.sleep(BrowserConstants.DEFAULT_WEBDRIVER_DELAY)
        except :
            try :
                browser.get(parsedUrl)
                time.sleep(BrowserConstants.DEFAULT_WEBDRIVER_LARGE_DELAY)
            except Exception as exception :
                raise Exception(f'Not possible to access {parsedUrl}. Cause: {exception}')
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

    @SimpleClientMethod(requestClass=[str, BrowserConstants.BOWSER_CLASS])
    def accessUrlInNewTab(self, url, browser):
        if ObjectHelper.isNotNone(url) :
            self.newTab(browser)
            return self.accessUrl(url, browser)

    @SimpleClientMethod(requestClass=[BrowserConstants.BOWSER_CLASS])
    def newTab(self, browser) :
        browser.execute_script("window.open();")
        time.sleep(BrowserConstants.DEFAULT_WEBDRIVER_DELAY)
        browser.switch_to.window(browser.window_handles[-1])
        time.sleep(BrowserConstants.DEFAULT_WEBDRIVER_DELAY_FRACTION)

    @SimpleClientMethod(requestClass=[str])
    def typeIn(self, text, element=None) :
        element.send_keys(Keys.CONTROL, 'a')
        element.send_keys(text)

    @SimpleClientMethod(requestClass=[str])
    def typeInAndHitEnter(self, text, element=None) :
        self.typeIn(text, element=element)
        element.send_keys(Keys.ENTER)
        time.sleep(BrowserConstants.DEFAULT_WEBDRIVER_DELAY_FRACTION)

    @SimpleClientMethod(requestClass=[BrowserConstants.BOWSER_CLASS])
    def hitControlV(self, browser, element=None) :
        webdriver.ActionChains(browser).key_down(Keys.CONTROL, element).send_keys('v').key_up(Keys.CONTROL, element).perform()
        time.sleep(BrowserConstants.DEFAULT_WEBDRIVER_DELAY_FRACTION)
        KeyboardUtil.esc()
        # actions.key_down(Keys.CONTROL)
        # actions.send_keys("v")
        # actions.key_up(Keys.CONTROL)
        # element.send_keys(Keys.ENTER)
        # ActionChains(driver).key_down(Keys.CONTROL, element).send_keys('v').key_up(Keys.CONTROL, element).perform()

    @SimpleClientMethod(requestClass=[BrowserConstants.BOWSER_CLASS]) ###- WebElement
    def hitControF5(self, browser) :
        # body = browser.find_element_by_tag_name('body')
        # webdriver.ActionChains(browser).key_down(Keys.CONTROL, body).send_keys(Keys.F5).key_up(Keys.CONTROL, body).perform()
        browser.switch_to.window(browser.current_window_handle)
        KeyboardUtil.ctrlF5()
        # browser.refresh()

    @SimpleClientMethod(requestClass=[BrowserConstants.BOWSER_CLASS]) ###- WebElement
    def hitF5(self, browser) :
        # body = browser.find_element_by_tag_name('body')
        # webdriver.ActionChains(browser).key_down(Keys.CONTROL, body).send_keys(Keys.F5).key_up(Keys.CONTROL, body).perform()
        # KeyboardUtil.ctrlF5()
        browser.refresh()

    @SimpleClientMethod(requestClass=[str, BrowserConstants.BOWSER_CLASS])
    def getAttribute(self, attributeName, element) :
        return element.get_attribute(attributeName)

    @SimpleClientMethod(requestClass=[str, BrowserConstants.BOWSER_CLASS])
    def findByXPath(self, xPath, browser) :
        element = browser.find_element_by_xpath(xPath)
        time.sleep(BrowserConstants.DEFAULT_WEBDRIVER_DELAY_FRACTION)
        return element

    @SimpleClientMethod(requestClass=[str, BrowserConstants.BOWSER_CLASS])
    def findAllByXPath(self, xPath, browser) :
        elementList = browser.find_elements_by_xpath(xPath)
        time.sleep(BrowserConstants.DEFAULT_WEBDRIVER_DELAY_FRACTION)
        return elementList

    @SimpleClientMethod(requestClass=[str, BrowserConstants.BOWSER_CLASS])
    def accessByXPath(self, xPath, browser) :
        element = self.findByXPath(xPath, browser)
        self.access(element)

    @SimpleClientMethod(requestClass=[BrowserConstants.BOWSER_CLASS])
    def access(self, element) :
        element.click()
        time.sleep(BrowserConstants.DEFAULT_WEBDRIVER_DELAY)
        return element

    @SimpleClientMethod(requestClass=[str, BrowserConstants.BOWSER_CLASS])
    def findByClass(self, className, browser) :
        if c.SPACE in className :
            return self.findByCss(StringHelper.join([c.NOTHING, *className.split()], character=c.DOT), browser)
        element = browser.find_element_by_class_name(className)
        time.sleep(BrowserConstants.DEFAULT_WEBDRIVER_DELAY_FRACTION)
        return element

    @SimpleClientMethod(requestClass=[str, BrowserConstants.BOWSER_CLASS])
    def findByCss(self, css, browser) :
        element = browser.find_element_by_css_selector(css)
        time.sleep(BrowserConstants.DEFAULT_WEBDRIVER_DELAY_FRACTION)
        return element

    @SimpleClientMethod(requestClass=[str, BrowserConstants.BOWSER_CLASS])
    def findByPartialClass(self, partialClass, browser, html=None) :
        elementList = self.findAllClassByPartialClass(partialClass, browser, html=html)
        if 1 <= len(elementList) :
            return elementList[0]

    @SimpleClientMethod(requestClass=[str, BrowserConstants.BOWSER_CLASS])
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

    @SimpleClientMethod(requestClass=[BrowserConstants.BOWSER_CLASS])
    def acceptAlert(self, browser):
        alert = browser.switch_to.alert
        alert.accept()
        time.sleep(BrowserConstants.DEFAULT_WEBDRIVER_DELAY)

    @SimpleClientMethod(requestClass=[BrowserConstants.BOWSER_CLASS])
    def maximize(self, browser) :
        browser.maximize_window()

    @SimpleClientMethod(requestClass=[BrowserConstants.BOWSER_CLASS])
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

        # Patch the function before creating the browser object
        RemoteWebDriver.execute = new_command_execute

        new_browser = webdriver.Remote(command_executor=executor_url, desired_capabilities={})
        new_browser.session_id = session_id

        # Replace the patched function with original function
        RemoteWebDriver.execute = org_command_execute

        return new_browser

    @SimpleClientMethod(requestClass=[str, str, BrowserConstants.BOWSER_CLASS])
    def screeshotWebPage(self, screenshotName, url, browser) :
        browser.get(url)
        time.sleep(BrowserConstants.DEFAULT_WEBDRIVER_DELAY_FRACTION)
        original_size = browser.get_window_size()
        required_width = browser.execute_script('return document.body.parentNode.scrollWidth')
        required_height = browser.execute_script('return document.body.parentNode.scrollHeight')
        browser.set_window_size(required_width, required_height)
        body = browser.find_element_by_tag_name('body')
        time.sleep(BrowserConstants.DEFAULT_WEBDRIVER_DELAY_FRACTION)
        body.screenshot(screenshotName)
        browser.set_window_size(original_size['width'], original_size['height'])
        return screenshotName
        # # browser.save_screenshot(path)  # has scrollbar
        # browser.find_element_by_tag_name('body').screenshot('ss.png')  # avoids scrollbar

    @SimpleClientMethod(requestClass=[str, BrowserConstants.BOWSER_CLASS])
    def pasteToBrowser(self, screenshotName, browser, element=None):
        image = Image.open(screenshotName)
        output = BytesIO()
        image.convert('RGB').save(output, 'BMP')
        data = output.getvalue()[14:]
        output.close()
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
        win32clipboard.CloseClipboard()
        self.hitControlV(browser, element=element)
        # KeyboardUtil.ctrlV()


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
