class MessageScanResponseDto :
    def __init__(self,
        key = None,
        html = None,
        errorList = None
    ) :
        self.key = key
        self.html = html
        self.errorList = errorList
