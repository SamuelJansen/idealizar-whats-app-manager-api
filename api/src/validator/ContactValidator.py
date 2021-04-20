from python_helper import ObjectHelper
from python_framework import Validator, ValidatorMethod, GlobalException, HttpStatus

import ContactDto

@Validator()
class ContactValidator:

    @ValidatorMethod(requestClass=[ContactDto.ContactRequestDto])
    def validateRequestDtoExists(self, dto) :
        self.validateKeyAndTypeNotNone(dto)
        if not self.service.contact.exists(dto) :
            raise GlobalException.GlobalException(
                message = f'''Contact '{dto.key}' not found''',
                status = HttpStatus.BAD_REQUEST
            )

    @ValidatorMethod(requestClass=[ContactDto.ContactRequestDto])
    def validateKeyAndTypeNotNone(self, dto) :
        if ObjectHelper.isNone(dto.key) :
            raise GlobalException.GlobalException(
                message = f'''The ContactDto.key '{dto.key}' cannot be None''',
                status = HttpStatus.BAD_REQUEST
            )
        if ObjectHelper.isNone(dto.type) :
            raise GlobalException.GlobalException(
                message = f'''The ContactDto.type '{dto.type}' cannot be None''',
                status = HttpStatus.BAD_REQUEST
            )
