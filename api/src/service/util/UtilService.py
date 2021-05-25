from python_framework import Service, ServiceMethod
from EncodeDecodeAction import EncodeDecodeAction
import Base64Dto

@Service()
class UtilService:

    @ServiceMethod(requestClass = [str, str])
    def encodeDecodeBase64(self, action, payload):
        if EncodeDecodeAction.ENCODE == action :
            return Base64Dto.Base64ResponseDto(self.helper.base64.encodeAndFilter(payload))
        elif EncodeDecodeAction.DECODE == action :
            return Base64Dto.Base64ResponseDto(self.helper.base64.decodeAndFilter(payload))
        raise Exception(f'EncodeDecodeAction not implemented: {action}')
