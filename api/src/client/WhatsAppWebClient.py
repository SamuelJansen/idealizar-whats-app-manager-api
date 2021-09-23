from python_helper import Constant as c
from python_helper import ObjectHelper, log, StringHelper
from python_framework import Client, ClientMethod, HttpStatus, GlobalException

import json
import requests

from config import WhatsAppWebConfig

SCAN_URL = f'{WhatsAppWebConfig.BASE_URL}/message/scan'
WRITE_URL = f'{WhatsAppWebConfig.BASE_URL}/message/write'
AUTHENTICATION_STATUS_URL = f'{WhatsAppWebConfig.BASE_URL}/authentication'

@Client()
class WhatsAppWebClient :

    @ClientMethod()
    def scanNewMessages(self, scanRequestDto) :
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        response = requests.patch(SCAN_URL, headers=headers, json=scanRequestDto, timeout=WhatsAppWebConfig.REQUEST_TIMEOUT)
        if 399 < response.status_code :
            raise GlobalException(
                message = self.getErrorMessage(response),
                status = HttpStatus.map(response.status_code),
                logMessage = 'Error at client call'
            )
        return response.json(), HttpStatus.map(response.status_code)

    @ClientMethod()
    def writeMessages(self, writeRequestDto) :
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        response = requests.patch(WRITE_URL, headers=headers, json=writeRequestDto, timeout=WhatsAppWebConfig.REQUEST_TIMEOUT)
        if 399 < response.status_code :
            raise GlobalException(
                message = self.getErrorMessage(response),
                status = HttpStatus.map(response.status_code),
                logMessage = 'Error at client call'
            )
        return response.json(), HttpStatus.map(response.status_code)

    @ClientMethod()
    def getAuthenticationStatus(self) :
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        response = requests.get(AUTHENTICATION_STATUS_URL, headers=headers, timeout=WhatsAppWebConfig.REQUEST_TIMEOUT)
        if 399 < response.status_code :
            raise GlobalException(
                message = self.getErrorMessage(response),
                status = HttpStatus.map(response.status_code),
                logMessage = 'Error at client call'
            )
        return response.json(), HttpStatus.map(response.status_code)

    def getErrorMessage(self, response) :
        errorMessage = 'Client did not sent any message'
        try :
            errorMessage = response.json()['message']
        except Exception as exception :
            log.warning(self.getErrorMessage, 'Not possible to get error message from response', exception=exception)
        return errorMessage
