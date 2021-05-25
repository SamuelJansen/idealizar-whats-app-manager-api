import time
from python_helper import Constant as c
from python_helper import ObjectHelper, log, StringHelper
from python_framework import Service, ServiceMethod, WebBrowser, Serializer

import DateTimeUtil

import PoolerConstants
from PoolingStatus import PoolingStatus

import Message, MessageConstants
import Session

import GoogleSearchConstants

import PoolerDto, ContactDto

WHATS_APP_URL = "https://web.whatsapp.com/"

# XPATH_IDEALIZAR_STUDENT_GROUP = '//div//div//span[@title="Idealizar SandBox - Test"]' ###- Idealizar - Estudantes ###- Groups
# XPATH_IDEALIZAR_BIRDMESSAGE_SANDBOX_GROUP = '//div//div//span//span[@title="+44 7418 310508"]' ###- Idealizar SandBox ###- Contact

XPATH_GROUP_MESSAGE_SECTION = '//div//div//div[@aria-label="Message list. Press right arrow key on a message to open message context menu."]'
XPATH_GROUP_MESSAGE_LIST = '//div[contains(@class,"focusable-list-item")]'
XPATH_TEXT_BOX = '//div//div//div[@contenteditable="true"]'
XPATH_SEND_IMAGE = '//div//div//span[@data-icon="send"]'

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

    @ServiceMethod()
    def inteigentLoop(self) :
        contactList = self.repository.contact.findAllByKeyIn([
            '+55 51 8029-8228'
            # '+55 51 8060-3925',
            # '+55 51 8559-9625',
            # '+55 51 9473-4741',
            # '+55 51 9871-9575',
            # '+55 51 9896-1495'
        ])
        idealizarGroup = self.repository.contact.findByKey('Idealizar - Estudantes')
        messageBird = self.repository.contact.findByKey('+44 7418 310508')
        for contact in contactList :
            try :
                self.poolMessagesFromOriginToDestiny(
                    self.mapper.contact.fromModelToRequestDto(contact),
                    self.mapper.contact.fromModelToRequestDto(idealizarGroup)
                )
            except Exception as exception :
                log.error(self.inteigentLoop, f'Not possible to pool messages from {[c.name for c in contactList]} to {idealizarGroup.name} properly', exception)
        try :
            self.poolMessagesFromOriginToDestiny(
                self.mapper.contact.fromModelToRequestDto(idealizarGroup),
                self.mapper.contact.fromModelToRequestDto(messageBird)
            )
        except Exception as exception :
            log.error(self.inteigentLoop, f'Not possible to pool messages from {idealizarGroup.name} to {messageBird.name}', exception)

    @ServiceMethod(requestClass=[ContactDto.ContactRequestDto, ContactDto.ContactRequestDto])
    def poolMessagesFromOriginToDestiny(self, origin, destiny) :
        self.openBrowserIfNedded(WHATS_APP_URL)
        if self.browserIsAvailable() :
            self.available = False
            log.debug(self.poolMessagesFromOriginToDestiny, f'pooling messages from {origin.key} to {destiny.key}')
            didAccessOrigin = self.safellyAccess(self.helper.whatsApp.getContactConversationXPath(origin))
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
                        # log.prettyPython(self.poolMessagesFromOriginToDestiny, "message", message.text, logLevel=log.DEBUG)
                        errorList = []
                        messageId = self.safellyGetMessageId(errorList, message=message)
                        if messageId in newMessageIdList or messageId.startswith(MessageConstants.ERROR_ID_STARTS_WITH) :
                            isPoolerMessage = self.safellyGetIsPoolerMessage(errorList, message=message)
                            ownerContent = self.safellyGetOwnerContent(errorList, message=message)
                            html = self.safellyGetAttribute(errorList, 'innerHTML', message=message)
                            owner = self.safellyGetOwner(errorList, lastOwner, ownerContent=ownerContent)
                            content = self.safellyGetContent(errorList, message=message, html=html)
                            poolingStatus = self.safellyGetPoolingStatus(errorList, content=content)
                            originalAsText = self.safellyGetOriginalAsText(errorList, message=message)
                            model = Message.Message(
                                messageId = messageId,
                                pooledAt = DateTimeUtil.dateTimeNow(),
                                isPoolerMessage = isPoolerMessage,
                                owner = owner,
                                content = content,
                                ownerContent = ownerContent,
                                originalAsText = originalAsText,
                                originalAsHtml = html,
                                poolingStatus = poolingStatus,
                                errorCount = len(errorList),
                                errorListAsJson = Serializer.jsonifyIt(errorList)
                            )
                            modelCreateList.append(model)
                            lastOwner = owner if ObjectHelper.isNotNone(owner) else lastOwner
                    self.service.message.createAll(modelCreateList)
                except Exception as exception :
                    log.error(self.poolMessagesFromOriginToDestiny, f'Not possible to poll messages from {origin.key} to {destiny.key}', exception)
                log.prettyPython(self.poolMessagesFromOriginToDestiny, "modelCreateList", modelCreateList, logLevel=log.DEBUG)
                modelUpdateList = []
                try :
                    textBox = self.client.browser.findAllByXPath(XPATH_TEXT_BOX,  self.browser)[-1]
                    self.client.browser.access(textBox)
                    for model in modelCreateList :
                        if self.isGoogleSearch(model) :
                            googleSearchDtoList = self.service.googleSearch.search(StringHelper.join(model.content.split()[2:], character=c.SPACE))
                            for googleSearchDto in googleSearchDtoList :
                                errorList = []
                                self.safellyTypeInAndHitEnter(errorList, model, googleSearchDto.suggestedText, textBox)
                                self.pasteScreenshot(googleSearchDto.screenshotName, element=textBox)
                                self.safellyAccess(XPATH_SEND_IMAGE)
                                self.client.browser.access(textBox)
                            model.poolingStatus = PoolingStatus.SUCCESS if ObjectHelper.isEmpty(errorList) else PoolingStatus.ERROR_DELIVERING
                            model.errorCount += len(errorList)
                            model.errorListAsJson += f' {c.OPEN_LIST}{model.errorListAsJson}, {Serializer.jsonifyIt(errorList)}{c.CLOSE_LIST}'
                            modelUpdateList.append(model)
                except Exception as exception :
                    log.error(self.poolMessagesFromOriginToDestiny, f'Not possible to answare google query from {origin.key} to {origin.key}', exception)
                try :
                    didAccessDestiny = self.safellyAccess(self.helper.whatsApp.getContactConversationXPath(destiny))
                    if didAccessDestiny :
                        textBox = self.client.browser.findAllByXPath(XPATH_TEXT_BOX,  self.browser)[-1]
                        self.client.browser.access(textBox)
                        for model in modelCreateList :
                            if self.isNewMessage(model) :
                                errorList = []
                                self.safellyTypeInAndHitEnter(errorList, model, model.content, textBox)
                                model.poolingStatus = PoolingStatus.SUCCESS if ObjectHelper.isEmpty(errorList) else PoolingStatus.ERROR_DELIVERING
                                model.errorCount += len(errorList)
                                model.errorListAsJson += f' {c.OPEN_LIST}{model.errorListAsJson}, {Serializer.jsonifyIt(errorList)}{c.CLOSE_LIST}'
                                modelUpdateList.append(model)
                        self.service.message.updateAll(modelUpdateList)
                except Exception as exception :
                    log.error(self.poolMessagesFromOriginToDestiny, f'Not possible to deliver messages from {origin.key} to {destiny.key}', exception)
            self.available = True

    @ServiceMethod(requestClass=[PoolerDto.PoolerRequestDto])
    def poolMessages(self, dto) :
        self.validator.pooler.validateRequestDtoExists(dto)
        self.poolMessagesFromOriginToDestiny(dto.originContactDto, dto.destinyContactDto)

    @ServiceMethod(requestClass=[[str], Message.Message, str])
    def safellyTypeInAndHitEnter(self, errorList, model, content, textBox=None) :
        try :
            content = content if ObjectHelper.isNotNone(content) else model.content
            self.client.browser.typeInAndHitEnter(f'''{model.content} - {content}''', textBox)
        except Exception as exception :
            errorList.append(str(exception))
            log.failure(self.safellyTypeInAndHitEnter, 'Failure', exception=exception)

    @ServiceMethod(requestClass=[Message.Message])
    def isNewMessage(self, model) :
        return not model.isPoolerMessage and 0 == model.errorCount and PoolingStatus.POOLING == model.poolingStatus

    @ServiceMethod(requestClass=[Message.Message])
    def isGoogleSearch(self, model) :
        return not model.isPoolerMessage and 0 == model.errorCount and PoolingStatus.GOOGLE_SEARCHING == model.poolingStatus

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
            log.failure(self.safellyGetOwnerContent, f'Not posible to get owner content from {message.text}', exception=exception)
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

    @ServiceMethod(requestClass=[[str]])
    def safellyGetPoolingStatus(self, errorList, content=None) :
        poolingStatus = None
        try :
            if ObjectHelper.isNone(content) :
                poolingStatus = PoolingStatus.ERROR_POOLING
            else :
                poolingStatus = PoolingStatus.GOOGLE_SEARCHING if content.lower().startswith(GoogleSearchConstants.SEARCH_KEYWORD) else PoolingStatus.POOLING
        except Exception as exception :
            errorList.append(str(exception))
            log.failure(self.safellyGetPoolingStatus, f'Not possible to evaluate PoolingStatus from {content} properlly', exception=exception)
        return poolingStatus

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
            self.client.browser.screeshotWebPage('QRCode.png', url, self.browser)
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

    @ServiceMethod(requestClass=[str])
    def safellyAccess(self, xPath) :
        didAccess = False
        try :
            self.client.browser.accessByXPath(xPath, self.browser)
            didAccess = True
        except Exception as exception :
            log.failure(self.safellyAccess, f'Not possible to access {xPath}', exception=exception)
        return didAccess

    @ServiceMethod(requestClass=[str])
    def pasteScreenshot(self, screenshotName, element=None) :
        self.client.browser.pasteToBrowser(screenshotName, self.browser, element=element)



################################################################################
# XPATH_MESSAGE_OWNER = '//div[@class="copyable-text"]'
# XPATH_MESSAGE_CONTENT = '//div[contains(@class, "copyable-text selectable-text")]'
# CSS_MESSAGE_OWNER = "div[class^='copyable-text']"
# CSS_MESSAGE_CONTENT = "div[class*='selectable-text copyable-text']"
# CSS_MESSAGE_CONTENT = "span.ltr"
# CSS_MESSAGE_CONTENT = "span[class*='selectable-text copyable-text']" ###- 'content' : message.find_element_by_css_selector(CSS_MESSAGE_CONTENT).text, ### works
