import base64
from python_helper import Constant as c
from python_framework import Helper, HelperMethod

BINARY_ENDOCE_START_SINGLE_QUOTE = f'b{c.SINGLE_QUOTE}'
BINARY_ENCODE_FINISH_SINGLE_QUOTE = f'{c.SINGLE_QUOTE}'
BINARY_ENDOCE_START_DOUBLE_QUOTE = f'b{c.DOUBLE_QUOTE}'
BINARY_ENCODE_FINISH_DOUBLE_QUOTE = f'{c.DOUBLE_QUOTE}'

@Helper()
class Base64Helper :

    @HelperMethod(requestClass=str)
    def removeBinaryTextFromPayloadIfNedded(self, payload) :
        if payload.startswith(BINARY_ENDOCE_START_SINGLE_QUOTE) and payload.endswith(BINARY_ENCODE_FINISH_SINGLE_QUOTE) :
            return payload[2:-1]
        if payload.startswith(BINARY_ENDOCE_START_DOUBLE_QUOTE) and payload.endswith(BINARY_ENCODE_FINISH_DOUBLE_QUOTE) :
            return payload[2:-1]
        return payload

    @HelperMethod(requestClass=str)
    def encode(self, payload) :
        return base64.b64encode(payload.encode(c.UTF_8))

    @HelperMethod(requestClass=str)
    def decode(self, payload) :
        return base64.b64decode(payload).decode(c.UTF_8)

    @HelperMethod(requestClass=str)
    def encodeAndFilter(self, payload) :
        return self.helper.base64.removeBinaryTextFromPayloadIfNedded(str(self.helper.base64.encode(payload)))

    @HelperMethod(requestClass=str)
    def decodeAndFilter(self, payload) :
        return self.helper.base64.removeBinaryTextFromPayloadIfNedded(self.helper.base64.decode(payload))
