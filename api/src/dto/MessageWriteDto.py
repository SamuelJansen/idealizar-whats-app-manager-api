class MessageWriteRequestDto :
    def __init__(self,
        text = None
    ) :
        self.text = text

class MessageWriteResponseDto :
    def __init__(self,
        errorList = None
    ) :
        self.errorList = errorList
