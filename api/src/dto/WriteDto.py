from converter.static import ContactConverterStatic, MessageConverterStatic

class WriteRequestDto :
    def __init__(self,
        contact = None,
        messageWriteList = None
    ) :
        self.contact = ContactConverterStatic.toRequestDto(contact)
        self.messageWriteList = MessageConverterStatic.toWriteRequestDtoList(messageWriteList)

class WriteResponseDto :
    def __init__(self,
        messageWriteList = None
    ) :
        self.messageWriteList = MessageConverterStatic.toWriteResponseDtoList(messageWriteList)
