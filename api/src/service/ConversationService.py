import time
from python_helper import Constant as c
from python_helper import ObjectHelper, log, StringHelper, DateTimeHelper
from python_framework import Service, ServiceMethod

import DateTimeUtil
from util import SoupUtil

from domain import ConversationConstants, MessageConstants

import Message

import PoolerDto, ContactDto

@Service()
class ConversationService:

    simultaneousRequests = 0

    def isAvailable(self) :
        return (
            self.simultaneousRequests < ConversationConstants.SCHEDULER_MAX_SIMULTANEOUS_INSTANCES - 1 and
            self.service.login.isAuthenticated()
        )

    @ServiceMethod()
    def inteligentLoop(self) :
        if self.isAvailable() :
            self.simultaneousRequests += 1
            try :
                contactList = self.repository.contact.findAllByKeyIn([
                    '+55 51 8029-8228',
                    '+55 51 3239-0620'
                ])
                idealizarHB = self.repository.contact.findByKey('Idealizar SandBox - HB')
                messageBird = self.repository.contact.findByKey('Idealizar SandBox') ###- self.repository.contact.findByKey('+44 7418 310508')
                whatsAppAssistant = self.repository.contact.findByKey('WhatsApp Assistant')
                self.poolMessagesFromOriginToDestiny(
                    self.mapper.contact.fromModelListToRequestDtoList(contactList),
                    self.mapper.contact.fromModelToRequestDto(idealizarHB)
                )
                self.poolMessagesFromOriginToDestiny(
                    self.mapper.contact.fromModelListToRequestDtoList([idealizarHB]),
                    self.mapper.contact.fromModelToRequestDto(messageBird)
                )
                self.poolMessagesFromOriginToDestiny(
                    self.mapper.contact.fromModelListToRequestDtoList([messageBird]),
                    self.mapper.contact.fromModelToRequestDto(idealizarHB)
                )
                self.getMessageModelList(self.mapper.contact.fromModelListToRequestDtoList([whatsAppAssistant]), replyGoogleSearch=True)
            except Exception as exception :
                log.failure(self.inteligentLoop, 'Error in conversation call', exception)
            self.simultaneousRequests -= 1

    @ServiceMethod(requestClass=[[ContactDto.ContactRequestDto], ContactDto.ContactRequestDto])
    def poolMessagesFromOriginToDestiny(self, originList, destiny) :
        # log.prettyPython(self.poolMessagesFromOriginToDestiny, 'scanResponseDto', scanResponseDto, logLevel=log.DEBUG)
        messageModelList = self.getMessageModelList(originList, replyGoogleSearch=True)
        # log.prettyPython(self.poolMessagesFromOriginToDestiny, f'Messages from {origin.key} to {destiny.key}', [m.text for m in messageModelList], logLevel=log.DEBUG)
        writeRequestDto = {
            "contact": {
              "key": destiny.key,
              "type": destiny.type,
              "accessTime": 0
            },
            'messageWriteList': [{'text':f'{m.ownerInfo}{c.COLON}{c.NEW_LINE}{m.text}'} for m in messageModelList if not m.isPoolerMessage and not self.service.googleSearch.isRequest(m.text)]
        }
        # log.prettyPython(self.poolMessagesFromOriginToDestiny, 'Error list', writeResponseDto['messageWriteList'], logLevel=log.DEBUG)
        writeResponseDto = self.service.message.writeMessages(writeRequestDto)
        return writeResponseDto

    @ServiceMethod(requestClass=[[ContactDto.ContactRequestDto]])
    def getMessageModelList(self, contactList, replyGoogleSearch=False) :
        messageModelList = []
        for contact in contactList :
            innerMessageModelList = []
            scanRequestDto = {
              "contact": {
                "key": contact.key,
                "type": contact.type,
                "accessTime": 0.05
              }
              , "lastMessageKey": self.service.message.getLastMessageKey(contact.key)
              , "maxScanIterations" : 2
            }
            # log.prettyPython(self.poolMessagesFromOriginToDestiny, 'scanRequestDto', scanRequestDto, logLevel=log.DEBUG)
            scanResponseDto = self.service.message.scanNewMessages(scanRequestDto)
            # log.prettyPython(self.poolMessagesFromOriginToDestiny, 'scanResponseDto', scanResponseDto, logLevel=log.DEBUG)
            messageScanDtoList = [] if ObjectHelper.isNone(scanResponseDto) or 'messageScanList' not in scanResponseDto else scanResponseDto['messageScanList']
            for messageScanDto in messageScanDtoList :
                self.service.message.addScannedMessage(innerMessageModelList, messageScanDto, contact.key)
            self.service.message.createAll(innerMessageModelList)
            messageModelList += innerMessageModelList
            if replyGoogleSearch :
                self.answareGoogleSearch(innerMessageModelList, contact)
        return messageModelList

    @ServiceMethod(requestClass=[[Message.Message], ContactDto.ContactRequestDto])
    def answareGoogleSearch(self, messageModelList, contact) :
        for messageModel in messageModelList :
            googleSearchList = []
            if not messageModel.isPoolerMessage and self.service.googleSearch.isRequest(messageModel.text) :
                googleSearchList.append({'text':StringHelper.join([gs.suggestedText for gs in self.service.googleSearch.search(messageModel.text)], 3*c.NEW_LINE)})
            if ObjectHelper.isNotEmpty(googleSearchList) :
                googleWriteRequestDto = {
                    "contact": {
                      "key": contact.key,
                      "type": contact.type,
                      "accessTime": 0
                    },
                    'messageWriteList': googleSearchList
                }
                self.service.message.writeMessages(googleWriteRequestDto)
