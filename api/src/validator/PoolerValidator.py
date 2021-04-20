from python_framework import Validator, ValidatorMethod, GlobalException, HttpStatus

import PoolerDto

@Validator()
class PoolerValidator:

    @ValidatorMethod(requestClass=[PoolerDto.PoolerRequestDto])
    def validateRequestDtoExists(self, dto) :
        # try :
        self.validator.contact.validateRequestDtoExists(dto.originContactDto)
        self.validator.contact.validateRequestDtoExists(dto.destinyContactDto)
        # except Exception as exception :
        #     raise GlobalException.GlobalException(
        #         message = f'Invalid request. Cause: {exception}',
        #         status = HttpStatus.BAD_REQUEST
        #     )
