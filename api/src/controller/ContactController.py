from python_framework import Controller, ControllerMethod, HttpStatus
import ContactDto

@Controller(url = '/contact', tag='Contact', description='Contact controller')
class ContactController:

    @ControllerMethod(url = '/',
        requestClass = ContactDto.ContactRequestDto,
        responseClass = ContactDto.ContactResponseDto
    )
    def put(self, dto):
        return self.service.contact.safellyCreateOrUpdate(dto), HttpStatus.OK

@Controller(url = '/contact/batch', tag='Contact', description='Contact controller')
class ContactBatchController:

    @ControllerMethod(url = '/',
        requestClass = [[ContactDto.ContactRequestDto]],
        responseClass = [[ContactDto.ContactResponseDto]]
    )
    def put(self, dtoList):
        return self.service.contact.safellyCreateOrUpdateAll(dtoList), HttpStatus.OK
