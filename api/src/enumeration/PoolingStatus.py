from python_framework import Enum, EnumItem

@Enum()
class PoolingStatusEnumeration :
    NONE = EnumItem()
    POOLING = EnumItem()
    GOOGLE_SEARCHING = EnumItem()
    ERROR_POOLING = EnumItem()
    ERROR_DELIVERING = EnumItem()
    SUCCESS = EnumItem()

PoolingStatus = PoolingStatusEnumeration()
