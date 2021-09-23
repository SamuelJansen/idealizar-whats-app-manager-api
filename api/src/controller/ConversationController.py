from python_framework import Controller, ControllerMethod, HttpStatus

from dto import WriteDto

@Controller(url = '/conversation', tag='Conversation', description='Conversation controller')
class ConversationController:

    @ControllerMethod(url = '/',
        requestClass = [[WriteDto.WriteRequestDto]],
        responseClass = [[WriteDto.WriteResponseDto]]
    )
    def post(self, dtoList):
        return self.service.conversation.inform(dtoList), HttpStatus.OK
