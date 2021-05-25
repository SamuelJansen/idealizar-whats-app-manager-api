from bs4 import BeautifulSoup
from python_helper import Constant as c
from python_helper import log, ReflectionHelper, ObjectHelper, StringHelper

def getSoupFromHtml(htmlAsString) :
    return BeautifulSoup(htmlAsString, 'html.parser')

def prettyPython(soup, logLevel=log.DEBUG) :
    if ObjectHelper.isNotNone(soup) :
        log.prettyPython(prettyPython, 'soup', soup.prettify(), logLevel=log.DEBUG)

def getText(soupElement) :
    # log.prettyPython(self.poolMessagesFromOriginToDestiny, 'soupElement', ReflectionHelper.getItNaked(soupElement), logLevel=log.DEBUG)
    # log.prettyPython(self.poolMessagesFromOriginToDestiny, 'soupElement.__dict__', soupElement.__dict__, logLevel=log.DEBUG)
    if ObjectHelper.isNotNone(soupElement) and not isinstance(soupElement, str):
        return soupElement.text ###- soupElement.string
    else :
        return str(soupElement)

def findByPartialAttributeValue(soup, tag, attributeName, partialAttributeValue) :
    if ObjectHelper.isNotNone(soup) :
        return soup.find(tag, attrs={attributeName: lambda e: partialAttributeValue in e if e else False})

def findAllByPartialAttributeValue(soup, tag, attributeName, partialAttributeValue)  :
    if ObjectHelper.isNotNone(soup) :
        return soup.find_all(tag, attrs={attributeName: lambda e: partialAttributeValue in e if e else False})

def findTag(soup, tag) :
    if ObjectHelper.isNotNone(soup) :
        return soup.find(tag)

def getValue(soupElement, attributeName) :
    if ObjectHelper.isNotNone(soupElement) and soupElement.has_attr(attributeName):
        value = soupElement[attributeName]
        return value if ObjectHelper.isNotList(value) else StringHelper.join(value, character=c.SPACE)
