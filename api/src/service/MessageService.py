from python_framework import Service, ServiceMethod

import DateTimeUtil

import Message

@Service()
class MessageService:

    @ServiceMethod(requestClass=[Message.Message])
    def create(self, model) :
        return self.repository.message.save(model)

    @ServiceMethod(requestClass=[[Message.Message]])
    def createAll(self, modelList) :
        return self.repository.message.saveAll(modelList)

    @ServiceMethod(requestClass=[[Message.Message]])
    def updateAll(self, modelList) :
        dateTimeNow = DateTimeUtil.dateTimeNow()
        for model in modelList :
            model.updatedAt = dateTimeNow
        return self.repository.message.saveAll(modelList)

    @ServiceMethod(requestClass=[[str]])
    def filterNewOnes(self, messageIdList) :
        return [messageId for messageId in messageIdList if self.isNewMessageId(messageId)]

    @ServiceMethod(requestClass=[str])
    def isNewMessageId(self, messageId) :
        return not self.repository.message.existsByMessageId(messageId)
