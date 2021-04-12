from python_framework import Controller, ControllerMethod, HttpStatus
import Base64Dto

@Controller(url = '/util', tag='Util', description='Util controller')
class Base64UtilController:

    @ControllerMethod(url = '/decode/<string:action>/<string:payload>',
        responseClass = Base64Dto.Base64ResponseDto
    )
    def get(self, action=None, payload=None):
        return self.service.util.encodeDecodeBase64(action, payload), HttpStatus.OK
