from python_framework import Controller, ControllerMethod, HttpStatus
import PoolerDto

@Controller(url = '/pooler', tag='Pooler', description='Pooler controller')
class PoolerController:

    @ControllerMethod(url = '/',
        requestClass = PoolerDto.PoolerRequestDto
    )
    def patch(self, dto):
        return self.service.pooler.poolMessagesFromOriginToDestiny(dto), HttpStatus.OK
