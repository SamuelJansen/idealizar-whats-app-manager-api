from python_framework import Service, ServiceMethod

from domain import LoginConstants
from enumeration.AuthenticationStatus import AuthenticationStatus
from dto import QRCodeDto

@Service()
class LoginService:

    @ServiceMethod()
    def isAuthenticated(self) :
        authenticationResponse = self.client.whatsAppWeb.getAuthenticationStatus()
        return AuthenticationStatus.map(authenticationResponse.get('status')) in [
            AuthenticationStatus.AUTHENTICATED,
            AuthenticationStatus.ALREADY_AUTHENTICATED
        ]

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
