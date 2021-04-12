from python_framework import Validator, ValidatorMethod, GlobalException, HttpStatus

import ContactDto

@Validator()
class PoolerValidator:

    @ValidatorMethod(requestClass=[ContactDto.ContactPoolerRequestDto, ContactDto.ContactPoolerRequestDto])
    def validateRequestDto(self, originDto, destinyDto) :
        self.validateRequestDtoAttributes(originDto, destinyDto)
        if not self.service.contact.exists(originDto) :
            raise GlobalException.GlobalException(
                message = f'The originDto "{originDto.key}" not found',
                status = HttpStatus.BAD_REQUEST
            )
        if not self.service.contact.exists(destinyDto) :
            raise GlobalException.GlobalException(
                message = f'The destinyDto "{destinyDto.key}" not found',
                status = HttpStatus.BAD_REQUEST
            )

    @ValidatorMethod(requestClass=[ContactDto.ContactPoolerRequestDto, ContactDto.ContactPoolerRequestDto])
    def validateRequestDtoAttributes(self, originDto, destinyDto) :
        if ObjectHelper.isNone(originDto.key) or ObjectHelper.isNone(destinyDto.key) :
            raise GlobalException.GlobalException(
                message = f'The originDto.key "{originDto.key}" and destinyDto.key "{destinyDto.key}" cannot be None',
                status = HttpStatus.BAD_REQUEST
            )
        if ObjectHelper.isNone(originDto.type) or ObjectHelper.isNone(destinyDto.type) :
            raise GlobalException.GlobalException(
                message = f'The originDto.type "{originDto.type}" and destinyDto.type "{destinyDto.type}" cannot be None',
                status = HttpStatus.BAD_REQUEST
            )
