from python_framework import Enum, EnumItem

@Enum()
class AuthenticationStatusEnumeration :
    NONE = EnumItem()
    AUTHENTICATED = EnumItem()
    ALREADY_AUTHENTICATED = EnumItem()
    NOT_AUTHENTICATED = EnumItem()

AuthenticationStatus = AuthenticationStatusEnumeration()
