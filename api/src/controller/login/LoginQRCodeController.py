from python_framework import Controller, ControllerMethod, HttpStatus

from dto import QRCodeDto

@Controller(url = '/login/qr-code', tag='Login', description='Login controller')
class LoginQRCodeController:

    @ControllerMethod(url = '/')
    def post(self):
        return self.service.login.initiateAuthenticationByQRCode(), HttpStatus.OK

    @ControllerMethod(url = '/',
        requestClass=[QRCodeDto.QRCodeRequestDto]
    )
    def put(self, dto):
        return self.service.login.createOrUpdateQRCode(dto), HttpStatus.OK

    @ControllerMethod(url = '/')
    def patch(self):
        return self.service.login.resumeAuthenticationByQRCode(), HttpStatus.OK
