import time
from python_helper import Constant as c
from python_helper import ObjectHelper, log, StringHelper
from python_framework import Service, ServiceMethod, WebBrowser, Serializer

import DateTimeUtil

import PoolerConstants
from PoolingStatus import PoolingStatus

import Message, MessageConstants
import Session

from domain import GoogleSearchConstants
import GoogleSearchDto

import PoolerDto, ContactDto

@Service()
class GoogleSearchService:

    browser = None
    booting = GoogleSearchConstants.DEFAULT_BROWSER_BOOTING_VALUE
    available = GoogleSearchConstants.DEFAULT_AVAILABLE_STATUS

    @ServiceMethod(requestClass=[str, str])
    def takeScreenshot(self, screenshotName, url) :
        self.openBrowserIfNedded(url)
        if self.browserIsAvailable() :
            self.available = False
            self.client.browser.screeshotWebPage(screenshotName, url, self.browser)
            self.available = True

    @ServiceMethod(requestClass=[str])
    def search(self, search) :
        googleSearchResponseList = self.client.googleSearch.rawTextSearch(search, 1, 10)
        # log.prettyPython(self.search, f'google query: {search}, googleSearchResponseList', googleSearchResponseList, logLevel=log.SUCCESS)
        dtoList = []
        if ObjectHelper.isEmpty(googleSearchResponseList):
            title = 'Sorry'
            url = 'http://google.com.br'
            snippet = 'No relevante results were found'
            screenshotName = f'none.png'
            dtoList.append(
                GoogleSearchDto.GoogleSearchResponseDto(
                    title = title,
                    url = url,
                    snippet = snippet,
                    suggestedText = f'''*Title:* {title}{c.NEW_LINE}*Link:* {url}{c.NEW_LINE}*Snipet:* {snippet}''',
                    screenshotName = screenshotName
                )
            )
        else:
            for googleSearchResponse in googleSearchResponseList :
                title = googleSearchResponse.get('title')
                url = googleSearchResponse.get('link')
                snippet = googleSearchResponse.get('snippet')
                screenshotName = f'{str(time.time()).replace(c.DOT,c.BLANK)}.png'
                # self.takeScreenshot(screenshotName, url)
                dtoList.append(
                    GoogleSearchDto.GoogleSearchResponseDto(
                        title = title,
                        url = url,
                        snippet = snippet,
                        # suggestedText = f'''Title: {title.replace(c.NEW_LINE, c.SPACE)}{c.SPACE_DASH_SPACE *3}Link: {url}{c.SPACE_DASH_SPACE *3}Snipet: {snippet.replace(c.NEW_LINE, c.SPACE)}''',
                        suggestedText = f'''*Title:* {title}{c.NEW_LINE}*Link:* {url}{c.NEW_LINE}*Snipet:* {snippet}''',
                        screenshotName = screenshotName
                    )
                )
        return dtoList

    @ServiceMethod(requestClass=[str])
    def isRequest(self, text) :
        return ObjectHelper.isNotNone(str) and text.lower().startswith(GoogleSearchConstants.SEARCH_KEYWORD)

    @ServiceMethod(requestClass=[str])
    def openBrowserIfNedded(self, url) :
        if not self.browserIsBooted() and not self.browserIsBooting() :
            self.booting = True
            self.browser = self.client.browser.getNewBrowser()
            self.client.browser.accessUrl(url, self.browser)
            time.sleep(GoogleSearchConstants.FIRST_ACCESS_TIMEOUT)
            self.booting = False
            self.available = True

    @ServiceMethod()
    def browserIsAvailable(self) :
        # print(f'self.browserIsAvailable: {self.available}')
        return self.browserIsBooted() and self.available

    @ServiceMethod()
    def browserIsBooted(self) :
        return ObjectHelper.isNotNone(self.browser)

    @ServiceMethod()
    def browserIsBooting(self) :
        return self.booting
