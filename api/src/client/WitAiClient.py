from python_helper import Constant as c
from python_helper import ObjectHelper, log, StringHelper
from python_framework import Client, ClientMethod, HttpStatus, GlobalException, Serializer

import json
import requests

from config import WitAiConfig

from dto.witai import WitAiDto

MESSAGE_URL = f'{WitAiConfig.BASE_URL}/message'

@Client()
class WitAiClient :

    @ClientMethod(
        requestClass=[WitAiDto.WitAiMessageParamsRequest],
        logRequest = True,
        logResponse = True
    )
    def evaluateText(self, witAiParamsRequest) :
        headers = {'Authorization': WitAiConfig.AUTHORIZATION, 'Content-type': 'application/json', 'Accept': 'text/plain'}
        params = Serializer.getObjectAsDictionary(witAiParamsRequest)
        params['v'] = str(WitAiConfig.APP_ID)
        response = requests.get(MESSAGE_URL, headers=headers, params=params)
        if 399 < response.status_code :
            raise GlobalException(
                message = self.getErrorMessage(response),
                status = HttpStatus.map(response.status_code),
                logMessage = 'Error at client call'
            )
        return response.json(), HttpStatus.map(response.status_code)

    def getErrorMessage(self, response) :
        errorMessage = 'WitAi did not sent any message'
        try :
            errorMessage = response.json()['error']
        except Exception as exception :
            log.warning(self.getErrorMessage, 'Not possible to get error message from response', exception=exception)
        return errorMessage
