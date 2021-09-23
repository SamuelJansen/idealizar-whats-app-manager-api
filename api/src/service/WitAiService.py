from python_helper import Constant as c
from python_helper import ObjectHelper, log, StringHelper, DateTimeHelper
from python_framework import Service, ServiceMethod, Serializer

import Message
from dto.witai import WitAiDto

import Message

@Service()
class WitAiService:

    @ServiceMethod(requestClass=[Message.Message])
    def evaluateMessageText(self, messageModel) :
        response = self.client.witAi.evaluateText(
            WitAiDto.WitAiMessageParamsRequest(
                text = messageModel.text
            )
        )
        return WitAiDto.WitAiMessageResponse(**response)
