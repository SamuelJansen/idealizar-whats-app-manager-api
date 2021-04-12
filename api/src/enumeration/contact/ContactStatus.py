from python_framework import Enum, EnumItem

@Enum()
class ContactStatusEnumeration :
    NONE = EnumItem()
    ACTIVE = EnumItem()
    INACTIVE = EnumItem()

ContactStatus = ContactStatusEnumeration()
