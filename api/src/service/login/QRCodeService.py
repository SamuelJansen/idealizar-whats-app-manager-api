from python_helper import Constant as c
from python_helper import ObjectHelper, log
from python_framework import Service, ServiceMethod

from domain import BrowserConstants, LoginConstants

from dto import QRCodeDto

@Service()
class QRCodeService:

    browser = None
    booting = BrowserConstants.DEFAULT_BROWSER_BOTTING_VALUE
    booted = BrowserConstants.DEFAULT_BOOTED_VALUE

    @ServiceMethod(requestClass=[QRCodeDto.QRCodeRequestDto])
    def save(self, dto) :
        return self.service.image.save(dto.qRCodeAsBase64, LoginConstants.QR_CODE_IMAGE_NAME)

    @ServiceMethod()
    def show(self) :
        if self.isAvailable() :
            self.accessUrl(LoginConstants.QR_CODE_AUTHENTICATION_PAGE)
            self.foceRefresh()
        else :
            self.openIfNedded()
            self.accessUrl(LoginConstants.QR_CODE_AUTHENTICATION_PAGE)

    @ServiceMethod()
    def foceRefresh(self) :
        self.client.browser.hitControF5(self.browser)

    @ServiceMethod()
    def closeQRCode(self) :
        self.tearDown()

    @ServiceMethod()
    def isBooting(self) :
        return self.booting

    @ServiceMethod()
    def isBooted() :
        return self.booted

    @ServiceMethod()
    def isAvailable(self) :
        return ObjectHelper.isNotNone(self.browser) and not self.isBooting()

    @ServiceMethod()
    def isNotAvailable(self) :
        return not self.isAvailable() or self.isBooting()

    @ServiceMethod()
    def openIfNedded(self, hidden=False) :
        log.log(self.openIfNedded, 'Started')
        if ObjectHelper.isNone(self.browser) and self.isNotBooting() :
            self.open(hidden=hidden)
        log.log(self.openIfNedded, 'Finished')

    @ServiceMethod()
    def open(self, hidden=False) :
        log.log(self.open, 'Started')
        self.booting = True
        self.safelyClose()
        self.browser = self.client.browser.getNewBrowser(hidden=hidden)
        self.client.browser.maximize(self.browser)
        sessionId = self.browser.session_id
        commandExecutor = self.browser.command_executor._url
        self.service.session.create(sessionId, commandExecutor)
        self.booted = True
        self.booting = False
        log.log(self.open, 'Finished')

    @ServiceMethod()
    def accessUrl(self, url) :
        self.client.browser.accessUrl(url, self.browser)

    @ServiceMethod()
    def tearDown(self) :
        log.log(self.tearDown, 'Started')
        self.safelyClose()
        log.log(self.tearDown, 'Finished')

    @ServiceMethod(requestClass=[str])
    def existsByXpath(self, xpath) :
        return self.client.browser.existsByXpath(xpath, self.browser)

    def safelyClose(self) :
        log.log(self.safelyClose, 'Started')
        if ObjectHelper.isNotNone(self.browser) :
            try :
                self.client.browser.close(self.browser)
            except Exception as exception :
                log.log(self.safelyClose, 'Not possible co close browser', exception=exception)
        self.browser = None
        self.booted = False
        log.log(self.safelyClose, 'Finished')

    @ServiceMethod()
    def isNotBooting(self) :
        return not self.isBooting()

    @ServiceMethod()
    def isNotBooted() :
        return not self.isBooted()
