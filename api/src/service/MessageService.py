from python_helper import Constant as c
from python_helper import ObjectHelper, log, StringHelper, DateTimeHelper
from python_framework import Service, ServiceMethod, Serializer

from util import SoupUtil
from enumeration.PoolingStatus import PoolingStatus

import Message

@Service()
class MessageService:

    simultaneousRequests = 0
    busy = False

    @ServiceMethod(requestClass=[Message.Message])
    def create(self, model) :
        return self.repository.message.save(model)

    @ServiceMethod(requestClass=[[Message.Message]])
    def createAll(self, modelList) :
        return self.repository.message.saveAll(modelList)

    @ServiceMethod(requestClass=[[Message.Message]])
    def updateAll(self, modelList) :
        dateTimeNow = DateTimeHelper.dateTimeNow()
        for model in modelList :
            model.updatedAt = dateTimeNow
        return self.repository.message.saveAll(modelList)

    @ServiceMethod(requestClass=[[str]])
    def filterNewOnes(self, keyList) :
        return [key for key in keyList if self.isNewKey(key)]

    @ServiceMethod(requestClass=[str])
    def isNewKey(self, key) :
        return not self.repository.message.existsByKey(key)

    @ServiceMethod(requestClass=[dict, str])
    def buildModelFromMessageScanResponseDto(self, messageScanDto, conversationKey) :
        errorList = messageScanDto['errorList']
        soup = SoupUtil.getSoupFromHtml(messageScanDto['html'])
        ownerInfo = SoupUtil.getText(
            SoupUtil.getValue(
                SoupUtil.findByPartialAttributeValue(soup, 'div', 'class', 'copyable-text'),
                'data-pre-plain-text'
            )
        )
        ownerKey = ownerInfo.split(']')[-1].strip()
        ownerKey = ownerKey if not ownerKey.endswith(':') else ownerKey[:-1]
        now = DateTimeHelper.dateTimeNow()
        postedAt = ownerInfo.split(']')[0].split('[')[-1].strip().split()
        postedAt = f'{StringHelper.join(postedAt[-1].split("/")[::-1], character="-")} {postedAt[0]}:{str(now).split(":")[-1]}'
        return Message.Message(
            key = messageScanDto['key'],
            conversationKey = conversationKey,
            ownerKey = ownerKey,
            postedAt = postedAt,
            ownerInfo = ownerInfo,
            scannedAt = now,
            text = SoupUtil.getText(SoupUtil.findByPartialAttributeValue(soup, 'span', 'class', 'selectable-text copyable-text')),
            originalAsText = SoupUtil.getText(soup),
            originalAsHtml = messageScanDto['html'],
            isPoolerMessage = 'message-out' in SoupUtil.getValue(SoupUtil.findTag(soup, 'div'), 'class'),
            poolingStatus = PoolingStatus.SUCCESS,
            errorCount = len(errorList),
            errorListAsJson = Serializer.jsonifyIt(errorList)
        )

    @ServiceMethod(requestClass=[str])
    def getLastMessageKey(self, conversationKey) :
        return None if not self.repository.message.existsConversation(conversationKey) else self.repository.message.findLastMessageKey(conversationKey)

    @ServiceMethod(requestClass=[dict])
    def scanNewMessages(self, scanRequestDto) :
        self.waitUntilIsNotBusy()
        self.setToBusy()
        exception = None
        try :
            scanResponseDto = self.client.whatsAppWeb.scanNewMessages(scanRequestDto)
        except Exception as e :
            exception = e
        self.setToNotBusy()
        if exception :
            raise exception
        return scanResponseDto

    @ServiceMethod(requestClass=[dict])
    def writeMessages(self, writeRequestDto) :
        self.waitUntilIsNotBusy()
        self.setToBusy()
        exception = None
        try :
            writeResponseDto = self.client.whatsAppWeb.writeMessages(writeRequestDto)
        except Exception as e :
            exception = e
        self.setToNotBusy()
        if exception :
            raise exception
        return writeResponseDto

    @ServiceMethod()
    def waitUntilIsNotBusy(self) :
        while self.isBusy() :
            pass

    @ServiceMethod()
    def isBusy(self) :
        return True and self.busy

    @ServiceMethod()
    def isNotBusy(self) :
        return not self.isBusy()

    @ServiceMethod()
    def setToBusy(self) :
        self.busy = True

    @ServiceMethod()
    def setToNotBusy(self) :
        self.busy = False
