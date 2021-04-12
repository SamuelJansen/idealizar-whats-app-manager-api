import time
from python_helper import Constant as c
from python_helper import ObjectHelper, log, StringHelper
from python_framework import Service, ServiceMethod, WebBrowser, Serializer

import DateTimeUtil

import PoolerConstants
from PoolingStatus import PoolingStatus

import Message, MessageConstants
import Session

import ContactDto

WHATS_APP_URL = "https://web.whatsapp.com/"

XPATH_IDEALIZAR_STUDENT_GROUP = '//div//div//span[@title="Idealizar SandBox - Test"]' ###- Idealizar - Estudantes ###- Groups
XPATH_IDEALIZAR_BIRDMESSAGE_SANDBOX_GROUP = '//div//div//span//span[@title="+44 7418 310508"]' ###- Idealizar SandBox ###- Contact
XPATH_GROUP_MESSAGE_SECTION = '//div//div//div[@aria-label="Message list. Press right arrow key on a message to open message context menu."]'
XPATH_GROUP_MESSAGE_LIST = '//div[contains(@class,"focusable-list-item")]'
XPATH_TEXT_BOX = '//div//div//div[@contenteditable="true"]'

CLASS_MESSAGE_OWNER = 'copyable-text'
CLASS_PARTIAL_MESSAGE_CONTENT = 'selectable-text copyable-text'

ATTR_MESSAGE_ID = 'data-id'
ATTR_OWNER_CONTENT = 'data-pre-plain-text'
ATTR_IS_POOLER_MESSAGE = 'class'

AUTHENTICATION_TIME_OUT = 7

@Service()
class PoolerService:

    browser = None
    booting = PoolerConstants.DEFAULT_BROWSER_BOOTING_VALUE
    available = PoolerConstants.DEFAULT_AVAILABLE_STATUS

    @ServiceMethod(requestClass=[ContactDto.ContactPoolerRequestDto, ContactDto.ContactPoolerRequestDto])
    def poolMessagesFromOriginToDestiny(self, originDto, destinyDto) :
        self.validatro.contact.validateRequestDto(originDto, destinyDto)
        print(originDto, destinyDto)

    @ServiceMethod()
    def poolGroupMessages(self) :
        self.openBrowserIfNedded(WHATS_APP_URL)
        if self.browserIsAvailable() :
            self.available = False
            xPathOrigin = XPATH_IDEALIZAR_BIRDMESSAGE_SANDBOX_GROUP
            # xPathOriginMessageList = XPATH_GROUP_MESSAGE_LIST
            xPathDestiny = XPATH_IDEALIZAR_STUDENT_GROUP
            # xPathDestinyMessageList = XPATH_GROUP_MESSAGE_LIST

            while True :
                # xPathOrigin, xPathOriginMessageList, xPathDestiny, xPathDestinyMessageList = xPathDestiny, xPathDestinyMessageList, xPathOrigin, xPathOriginMessageList
                xPathOrigin, xPathDestiny = self.swap(xPathOrigin, xPathDestiny)
                didAccessOrigin = self.safellyAccess(xPathOrigin)
                if didAccessOrigin :
                    messageList = self.client.browser.findAllByXPath(XPATH_GROUP_MESSAGE_LIST, self.browser)
                    messageDictionary = {}
                    lastOwner = MessageConstants.UNKNOWN_OWNER
                    modelCreateList = []
                    modelDictionary = {}
                    try :
                        for message in messageList :
                            errorList = []
                            messageId = self.safellyGetMessageId(errorList, message=message)
                            if ObjectHelper.isNotNone(messageId) :
                                modelDictionary[messageId] = message
                            # else :
                            #     ownerContent = self.safellyGetOwnerContent(errorList, message=message)
                            #     owner = self.safellyGetOwner(errorList, lastOwner, ownerContent=ownerContent)
                            #     html = self.safellyGetAttribute(errorList, 'innerHTML', message=message)
                            #     originalAsText = self.safellyGetOriginalAsText(errorList, message=message)
                            #     content = self.safellyGetContent(errorList, message=message, html=html)
                            #     self.service.message.create(
                            #         Message.Message(
                            #             messageId = messageId,
                            #             pooledAt = DateTimeUtil.dateTimeNow(),
                            #             owner = owner,
                            #             content = content,
                            #             ownerContent = ownerContent,
                            #             originalAsText = originalAsText,
                            #             originalAsHtml = html,
                            #             poolingStatus = PoolingStatus.POOLING,
                            #             errorCount = len(errorList)
                            #         )
                            #     )
                        newMessageIdList = self.service.message.filterNewOnes(list(modelDictionary.keys()))

                        for collectedMessageId, message in modelDictionary.items() :
                            # log.prettyPython(self.poolGroupMessages, "message", message.text, logLevel=log.DEBUG)
                            errorList = []
                            messageId = self.safellyGetMessageId(errorList, message=message)
                            if messageId in newMessageIdList or messageId.startswith(MessageConstants.ERROR_ID_STARTS_WITH) :
                                isPoolerMessage = self.safellyGetIsPoolerMessage(errorList, message=message)
                                ownerContent = self.safellyGetOwnerContent(errorList, message=message)
                                html = self.safellyGetAttribute(errorList, 'innerHTML', message=message)
                                owner = self.safellyGetOwner(errorList, lastOwner, ownerContent=ownerContent)
                                content = self.safellyGetContent(errorList, message=message, html=html)
                                originalAsText = self.safellyGetOriginalAsText(errorList, message=message)
                                model = Message.Message(
                                    messageId = messageId,
                                    pooledAt = DateTimeUtil.dateTimeNow(),
                                    isPoolerMessage = self.safellyGetIsPoolerMessage(errorList, message=message),
                                    owner = owner,
                                    content = self.safellyGetContent(errorList, message=message, html=html),
                                    ownerContent = ownerContent,
                                    originalAsText = originalAsText,
                                    originalAsHtml = html,
                                    poolingStatus = PoolingStatus.POOLING,
                                    errorCount = len(errorList),
                                    errorListAsJson = Serializer.jsonifyIt(errorList)
                                )
                                modelCreateList.append(model)
                                lastOwner = owner if ObjectHelper.isNotNone(owner) else lastOwner
                        self.service.message.createAll(modelCreateList)
                    except Exception as exception :
                        log.error(self.poolGroupMessages, f'Not possible to poll messages from {xPathOrigin} to {xPathDestiny}', exception)
                    log.prettyPython(self.poolGroupMessages, "modelCreateList", modelCreateList, logLevel=log.DEBUG)
                    try :
                        didAccessDestiny = self.safellyAccess(xPathDestiny)
                        if didAccessDestiny :
                            textBox = self.client.browser.findAllByXPath(XPATH_TEXT_BOX,  self.browser)[-1]
                            self.client.browser.access(textBox)
                            modelUpdateList = []
                            for model in modelCreateList :
                                if self.isNewMessage(model) :
                                    errorList = []
                                    # self.client.browser.typeIn(f'''{model.owner} - {model.content}''', textBox)
                                    self.safellyTypeInAndHitEnter(errorList, model, textBox)
                                    model.poolingStatus = PoolingStatus.SUCCESS if ObjectHelper.isEmpty(errorList) else PoolingStatus.ERROR_DELIVERING
                                    model.errorCount += len(errorList)
                                    model.errorListAsJson += f' {c.OPEN_LIST}{model.errorListAsJson}, {Serializer.jsonifyIt(errorList)}{c.CLOSE_LIST}'
                                    modelUpdateList.append(model)
                            self.service.message.updateAll(modelUpdateList)
                    except Exception as exception :
                        log.error(self.poolGroupMessages, f'Not possible to deliver messages from {xPathOrigin} to {xPathDestiny}', exception)
            self.available = True

    @ServiceMethod(requestClass=[[str], Message.Message])
    def safellyTypeInAndHitEnter(self, errorList, model, textBox=None) :
        try :
            self.client.browser.typeInAndHitEnter(f'''{model.owner} - {model.content}''', textBox)
        except Exception as exception :
            errorList.append(str(exception))
            log.failure(self.safellyTypeInAndHitEnter, 'Failure', exception=exception)

    @ServiceMethod(requestClass=[Message.Message])
    def isNewMessage(self, model) :
        return not model.isPoolerMessage and 0 == model.errorCount

    @ServiceMethod(requestClass=[[str]])
    def safellyGetIsPoolerMessage(self, errorList, message=None) :
        isPoolerMessage = False
        try :
            attributeValue = self.client.browser.getAttribute(ATTR_IS_POOLER_MESSAGE, message)
            isPoolerMessage = 'message-out' in attributeValue
        except Exception as exception :
            errorList.append(str(exception))
            log.failure(self.safellyGetIsPoolerMessage, 'Failure', exception=exception)
        return isPoolerMessage

    @ServiceMethod(requestClass=[[str]])
    def safellyGetMessageId(self, errorList, message=None) :
        messageId = None
        try :
            messageId = self.client.browser.getAttribute(ATTR_MESSAGE_ID, message)
        except Exception as exception :
            errorList.append(str(exception))
            log.failure(self.safellyGetMessageId, 'Failure', exception=exception)
        return messageId

    @ServiceMethod(requestClass=[[str]])
    def safellyGetOwnerContent(self, errorList, message=None) :
        ownerContent = None
        try :
            ownerContent = self.client.browser.getAttribute(
                ATTR_OWNER_CONTENT,
                self.client.browser.findByClass(
                    CLASS_MESSAGE_OWNER,
                    message
                )
            )
        except Exception as exception :
            errorList.append(str(exception))
            log.failure(self.safellyGetOwnerContent, 'Failure', exception=exception)
        return ownerContent

    @ServiceMethod(requestClass=[[str], str])
    def safellyGetOwner(self, errorList, lastOwner, ownerContent=None) :
        if ObjectHelper.isNotNone(ownerContent) :
            owner = None
            try :
                if c.CLOSE_LIST in ownerContent :
                    owner = StringHelper.join(ownerContent.split(c.CLOSE_LIST)[1:], character=c.SPACE).strip()
                    if owner.endswith(c.COLON) :
                        owner = owner[:-1]
                else :
                    owner = ownerContent.strip()
            except Exception as exception :
                errorList.append(str(exception))
                log.failure(self.safellyGetOwner, 'Failure', exception=exception)
            return owner

    @ServiceMethod(requestClass=[[str]])
    def safellyGetOriginalAsText(self, errorList, message=None) :
        text = None
        try :
            text = message.text
        except Exception as exception :
            errorList.append(str(exception))
            log.failure(self.safellyGetOriginalAsText, 'Failure', exception=exception)
        return text

    @ServiceMethod(requestClass=[[str]])
    def safellyGetContent(self, errorList, message=None, html=None) :
        content = None
        try :
            content = self.client.browser.findByPartialClass(CLASS_PARTIAL_MESSAGE_CONTENT, message, html=html).text
        except Exception as exception :
            errorList.append(str(exception))
            log.failure(self.safellyGetContent, 'Failure', exception=exception)
        return content

    def safellyGetAttribute(self, errorList, attributeName, message=None) :
        attributeValue = None
        try :
            attributeValue = self.client.browser.getAttribute(attributeName, message)
        except Exception as exception :
            errorList.append(str(exception))
            log.failure(self.safellyGetAttribute, 'Failure', exception=exception)
        return attributeValue

    @ServiceMethod(requestClass=[str])
    def openBrowserIfNedded(self, url) :
        if not self.browserIsBooted() and not self.browserIsBooting() :
            self.booting = True
            # mostRecentSession = self.service.session.findMostRecent()
            # if ObjectHelper.isNone(mostRecentSession) :
            #     self.browser = self.client.browser.getNewBrowser()
            #     self.service.session.create(
            #         Session.Session(
            #             sessionId = self.browser.session_id,
            #             commandExecutor = self.browser.command_executor._url
            #         )
            #     )
            # else :
            #     self.browser = self.client.browser.retrieveBrowserSession(mostRecentSession.sessionId, mostRecentSession.commandExecutor)
            self.browser = self.client.browser.getNewBrowser()
            self.service.session.create(
                Session.Session(
                    sessionId = self.browser.session_id,
                    commandExecutor = self.browser.command_executor._url
                )
            )
            self.client.browser.accessUrl(url, self.browser)
            time.sleep(AUTHENTICATION_TIME_OUT)
            self.booting = False
            self.available = True

    @ServiceMethod()
    def browserIsBooted(self) :
        return ObjectHelper.isNotNone(self.browser)

    @ServiceMethod()
    def browserIsBooting(self) :
        return self.booting

    @ServiceMethod()
    def browserIsAvailable(self) :
        # print(f'self.browserIsAvailable: {self.available}')
        return self.browserIsBooted() and self.available

    @ServiceMethod()
    def swap(self, xPathOrigin, xPathDestiny) :
        return xPathDestiny, xPathOrigin

    @ServiceMethod(requestClass=[str])
    def safellyAccess(self, xPath) :
        didAccess = False
        try :
            self.client.browser.accessByXPath(xPath, self.browser)
            didAccess = True
        except Exception as exception :
            log.failure(self.safellyAccess, f'Not possible to access {xPath}', exception=exception)
        return didAccess




################################################################################
# XPATH_MESSAGE_OWNER = '//div[@class="copyable-text"]'
# XPATH_MESSAGE_CONTENT = '//div[contains(@class, "copyable-text selectable-text")]'
# CSS_MESSAGE_OWNER = "div[class^='copyable-text']"
# CSS_MESSAGE_CONTENT = "div[class*='selectable-text copyable-text']"
# CSS_MESSAGE_CONTENT = "span.ltr"
# CSS_MESSAGE_CONTENT = "span[class*='selectable-text copyable-text']" ###- 'content' : message.find_element_by_css_selector(CSS_MESSAGE_CONTENT).text, ### works
