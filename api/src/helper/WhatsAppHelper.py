from python_helper import Constant as c
from python_framework import Helper, HelperMethod

import ContactDto, ContactConstants
from ContactType import ContactType
from ContactStatus import ContactStatus

@Helper()
class WhatsAppHelper :

    @HelperMethod(requestClass=ContactDto.ContactRequestDto)
    def getContactConversationXPath(self, dto) :
        if ContactType.USER == dto.type :
            return ContactConstants.XPATH_USER.replace(ContactConstants.TOKEN_CONTACT_KEY, dto.key)
        if ContactType.GROUP == dto.type :
            return ContactConstants.XPATH_GROUP.replace(ContactConstants.TOKEN_CONTACT_KEY, dto.key)
