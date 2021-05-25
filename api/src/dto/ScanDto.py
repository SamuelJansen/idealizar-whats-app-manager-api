from converter.static import ContactConverterStatic, ScanConverterStatic, MessageConverterStatic

class ScanRequestDto :
    def __init__(self,
        contact = None,
        lastMessageKey = None,
        maxScanIterations = None
    ) :
        self.contact = ContactConverterStatic.toRequestDto(contact)
        self.lastMessageKey = lastMessageKey
        self.maxScanIterations = ScanConverterStatic.getMaxScanIterations(maxScanIterations)

class ScanResponseDto :
    def __init__(self,
        messageScanList = None
    ) :
        self.messageScanList = MessageConverterStatic.toReadResponseDtoList(messageScanList)
