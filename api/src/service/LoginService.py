from python_framework import Service, ServiceMethod

from domain import LoginConstants
from dto import QRCodeDto

@Service()
class LoginService:

    @ServiceMethod()
    def initiateAuthenticationByQRCode(self) :
        self.service.qRCode.openIfNedded()
        self.service.qRCode.foceRefresh()

    @ServiceMethod(requestClass=[QRCodeDto.QRCodeRequestDto])
    def createOrUpdateQRCode(self, dto) :
        self.service.qRCode.save(dto)
        self.service.qRCode.show()

    @ServiceMethod()
    def resumeAuthenticationByQRCode(self) :
        self.service.qRCode.closeQRCode()
