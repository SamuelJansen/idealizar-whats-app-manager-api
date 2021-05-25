from python_framework import Serializer
import ContactDto

class PoolerRequestDto :
    def __init__(self,
        originContactDto = None,
        destinyContactDto = None
    ) :
        self.originContactDto = convertToContactDto(originContactDto)
        self.destinyContactDto = convertToContactDto(destinyContactDto)

def convertToContactDto(value) :
    if isinstance(value, ContactDto.ContactRequestDto) :
        return value
    else :
        returnValue = None
        try :
            returnValue = Serializer.convertFromJsonToObject(Serializer.getObjectAsDictionary(value), ContactDto.ContactRequestDto)
        except :
            returnValue = value
        return returnValue
