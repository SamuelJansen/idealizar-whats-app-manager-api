from python_framework import Enum, EnumItem

@Enum()
class ContactTypeEnumeration :
    NONE = EnumItem()
    USER = EnumItem()
    GROUP = EnumItem()

ContactType = ContactTypeEnumeration()
