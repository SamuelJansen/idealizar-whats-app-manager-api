from python_framework import Enum, EnumItem

@Enum()
class EncodeDecodeActionEnumeration :
    ENCODE = EnumItem()
    DECODE = EnumItem()

EncodeDecodeAction = EncodeDecodeActionEnumeration()
