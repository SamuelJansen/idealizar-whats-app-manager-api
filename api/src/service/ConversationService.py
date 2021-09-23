import time
from python_helper import Constant as c
from python_helper import ObjectHelper, log, StringHelper, DateTimeHelper
from python_framework import Service, ServiceMethod, Serializer

import DateTimeUtil
from util import SoupUtil

from domain import ConversationConstants, MessageConstants

from dto import WriteDto
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
                    'Ciência de Dados e IA'
                ])

                # idealizarHB = self.repository.contact.findByKey('Idealizar SandBox - HB')
                # messageBird = self.repository.contact.findByKey('Idealizar SandBox') ###- self.repository.contact.findByKey('+44 7418 310508')
                # whatsAppAssistant = self.repository.contact.findByKey('WhatsApp Assistant')
                # idealizarEstudantes = self.repository.contact.findByKey('Idealizar - Estudantes')

                # self.poolMessagesFromOriginToDestiny(
                #     self.mapper.contact.fromModelListToRequestDtoList(contactList),
                #     self.mapper.contact.fromModelToRequestDto(idealizarHB)
                # )
                # self.poolMessagesFromOriginToDestiny(
                #     self.mapper.contact.fromModelListToRequestDtoList([idealizarHB]),
                #     self.mapper.contact.fromModelToRequestDto(messageBird)
                # )
                # self.poolMessagesFromOriginToDestiny(
                #     self.mapper.contact.fromModelListToRequestDtoList([messageBird]),
                #     self.mapper.contact.fromModelToRequestDto(idealizarHB)
                # )
                self.getMessageModelList(self.mapper.contact.fromModelListToRequestDtoList(contactList), replyGoogleSearch=True)
                # self.getMessageModelList(self.mapper.contact.fromModelListToRequestDtoList([whatsAppAssistant]), replyGoogleSearch=True)
                # self.getMessageModelList(self.mapper.contact.fromModelListToRequestDtoList([idealizarEstudantes]), replyGoogleSearch=True)
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
            'messageWriteList': [{'text':f'{m.ownerInfo}{c.NEW_LINE}{m.text}'} for m in messageModelList if not m.isPoolerMessage and not self.service.googleSearch.isRequest(m.text)]
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
                messageModel = self.service.message.buildModelFromMessageScanResponseDto(messageScanDto, contact.key)
                innerMessageModelList.append(messageModel)
            self.service.message.createAll(innerMessageModelList)
            messageModelList += innerMessageModelList
            if replyGoogleSearch :
                self.answareGoogleSearch(innerMessageModelList, contact)
            self.answareWitAiQuestion(innerMessageModelList, contact)
        return messageModelList

    @ServiceMethod(requestClass=[[Message.Message], ContactDto.ContactRequestDto])
    def answareGoogleSearch(self, messageModelList, contact) :
        for messageModel in messageModelList :
            googleResponse = None
            if not messageModel.isPoolerMessage and self.service.googleSearch.isRequest(messageModel.text) :
                writeMessageRequestDto = {'text':StringHelper.join([gs.suggestedText for gs in self.service.googleSearch.search(messageModel.text)], 3*c.NEW_LINE)}
                if ObjectHelper.isNotNone(writeMessageRequestDto) :
                    writeRequestDto = {
                        "contact": {
                          "key": contact.key,
                          "type": contact.type,
                          "accessTime": 0
                        },
                        'messageWriteList': [writeMessageRequestDto]
                    }
                    self.service.message.writeMessages(writeRequestDto)

    @ServiceMethod(requestClass=[[Message.Message], ContactDto.ContactRequestDto])
    def answareWitAiQuestion(self, messageModelList, contact) :
        for messageModel in messageModelList :
            if not messageModel.isPoolerMessage :
                witAiResponse = self.service.witAi.evaluateMessageText(messageModel)
                log.prettyPython(self.answareWitAiQuestion, 'witAiResponse', witAiResponse.__dict__, logLevel=log.SUCCESS)
                if 0 < len(witAiResponse.intentList) :
                    # print(witAiResponse.__dict__)
                    if 'agenda' == witAiResponse.intentList[0]['name'] and ObjectHelper.isNotEmpty([r for r in witAiResponse.entityDictionary.get('wit$agenda_entry:agenda_entry', []) if 'reunião' == r.get('body', c.BLANK).lower() and r['confidence'] > .92]):
                        import requests
                        from config import IdealizaAgendaApiConfig
                        resp = requests.get(
                            f'{IdealizaAgendaApiConfig.BASE_URL}/agenda/ai',
                            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'},
                            timeout = IdealizaAgendaApiConfig.REQUEST_TIMEOUT
                        )
                        print(resp.json())
                        # print(type(resp.json()))
                        writeMessageRequestDto = {'text': StringHelper.join(
                            [f"Date: {r['beginAtDate']} {r['beginAtTime']}{c.NEW_LINE}About: {r['notes']}{c.NEW_LINE}Hoster: {r['hoster']}{c.NEW_LINE}Url: {r['url']}" for r in resp.json()],
                            character = 2*c.NEW_LINE
                        )}
                        # print(writeMessageRequestDto)
                        if ObjectHelper.isNotNone(writeMessageRequestDto) :
                            writeRequestDto = {
                                "contact": {
                                  "key": contact.key,
                                  "type": contact.type,
                                  "accessTime": 0
                                },
                                'messageWriteList': [writeMessageRequestDto]
                            }
                            self.service.message.writeMessages(writeRequestDto)

    @ServiceMethod()
    def checkAndInform(self) :
        import requests
        possiblePresentCall = requests.get('https://idealizar.glitch.me/dev-idealizar-agenda-api/agenda/present', timeout=3)
        responseList = []
        try :
            if possiblePresentCall and 399 >= possiblePresentCall.status_code :
                agendaRequestDto = possiblePresentCall.json()
                writeRequestDto = {
                    "contact": {
                      "key": 'Idealizar - Estudantes',
                      "type": 'GROUP',
                      "accessTime": 0
                    },
                    'messageWriteList': [{'text':f"Date: {agendaRequestDto['beginAtDate']} {agendaRequestDto['beginAtTime']}{c.NEW_LINE}About: {agendaRequestDto['notes']}{c.NEW_LINE}Hoster: {agendaRequestDto['hoster']}{c.NEW_LINE}Url: {agendaRequestDto['url']}"}]
                }
                responseList.append(self.service.message.writeMessages(writeRequestDto))
        except Exception as exception :
            log.failure(self.checkAndInform, 'Error in checkAndInform', exception)
        return Serializer.convertFromJsonToObject(responseList, [[WriteDto.WriteResponseDto]])
