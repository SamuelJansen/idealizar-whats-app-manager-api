from python_helper import EnvironmentHelper
from python_framework import Enum, EnumItem

@Enum(associateReturnsTo='credential')
class GoogleCredentialsEnumeration :
    CUSTOM_SEARCH_API_KEY = EnumItem(credential=EnvironmentHelper.get('GOOGLE_CUSTOM_SEARCH_API_KEY'))
    CUSTOM_SEARCH_CSE_ID = EnumItem(credential=EnvironmentHelper.get('GOOGLE_CUSTOM_SEARCH_CSE_ID'))

GoogleCredentials = GoogleCredentialsEnumeration()
