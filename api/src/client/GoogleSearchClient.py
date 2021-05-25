from python_helper import Constant as c
from python_helper import StringHelper, EnvironmentHelper, SettingHelper, ObjectHelper, log, ReflectionHelper
from python_framework import SimpleClient, SimpleClientMethod

from apiclient.discovery import build
import requests
import bs4

import GoogleSearchConstants
from GoogleCredentials import GoogleCredentials

@SimpleClient()
class GoogleSearchClient:

    ###- https://gist.github.com/nikhilkumarsingh/5bce182ed57ae73f6cbde52fe846991b
    google = None

    @SimpleClientMethod(requestClass=[str, int, int])
    def rawTextSearch(self, search, start, ammount) :
        if self.google is None :
            self.google = build("customsearch", 'v1', developerKey=GoogleCredentials.CUSTOM_SEARCH_API_KEY).cse()
        search = search if not search.startswith(GoogleSearchConstants.SEARCH_KEYWORD) else search[len(GoogleSearchConstants.SEARCH_KEYWORD):]
        result = self.google.list(q=search, cx=GoogleCredentials.CUSTOM_SEARCH_CSE_ID, lr='lang_pt', start=start, num=ammount).execute()
        return result.get('items', [])

    @SimpleClientMethod(requestClass=[str])
    def textSearch(self, link) :
        res = requests.get(link)
        soup = bs4.BeautifulSoup(res.content, "html.parser")
        return self.getText(self.getTag(link, soup.body))

    @SimpleClientMethod(requestClass=[str])
    def getText(self, tag) :
        text = StringHelper.join(
            [str(t) for t in tag.strings if StringHelper.isNotBlank(StringHelper.join(str(t).split(), character=c.BLANK).replace(c.SPACE, c.BLANK))],
            character=c.NEW_LINE
        )
        constant = 40
        for i in range(constant) :
            if i < constant - 1 :
                text = text.replace(GoogleSearchConstants.TOKENT_TEXT_SEPARATOR * (constant - i), c.BLANK)
            else :
                text = text.replace(GoogleSearchConstants.TOKENT_TEXT_SEPARATOR, c.SPACE)
        return text

    @SimpleClientMethod(requestClass=[str])
    def getTag(self, link, soupBody=None) :
        result = None
        if ObjectHelper.isNotNone(link) :
            for font in GoogleSearchConstants.POSSIBLE_FONTS :
                if link.startswith(font) :
                    result = self.getResult(
                        soup.find_all(
                            GoogleSearchConstants.POSSIBLE_FONTS[font][GoogleSearchConstants.KEY_TAG],
                            GoogleSearchConstants.POSSIBLE_FONTS[font][GoogleSearchConstants.KEY_ATTRIBUTE]
                        )
                    )
                    break
        return result if ObjectHelper.isNotNone(result) else soupBody

    @SimpleClientMethod(requestClass=[[str]])
    def getResult(self, resultList) :
        return None if ObjectHelper.isEmpty(resultList) or (isinstance(resultList, bs4.element.ResultSet) and 0 == len(resultList)) else resultList[0]


################################################################################
# Alternatives for google api:
#https://pypi.org/project/google-search/
# importing the module
# from googlesearch import search
# # stored queries in a list
# search_list = ["News","Share price forecast","Technical Analysis"]
# # save the company name in a variable
# company_name = input("Please provide the stock name:")
# # iterate through different keywords, search and print
# for j in search_list:
#    for i in search(company_name+j,  tld='com', lang='en', num=1, start=0, stop=1, pause=2.0):
#       print (i)
