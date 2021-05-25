from python_framework import Converter, ConverterMethod

from dto import ScanDto, MessageScanDto

@Converter()
class ScanConverter:

    @ConverterMethod(requestClass=[[MessageScanDto.MessageScanResponseDto]])
    def toResponseDto(self, messageResponseDtoList) :
        return ScanDto.ScanResponseDto(
            messageScanList = messageResponseDtoList
        )
