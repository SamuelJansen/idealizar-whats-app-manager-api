from ContactType import ContactType
from ContactStatus import ContactStatus

DEFAULT_TYPE = ContactType.NONE
DEFAULT_STATUS = ContactStatus.NONE

TOKEN_CONTACT_KEY = '__TOKEN_CONTACT_KEY__'
XPATH_GROUP = f'//div//div//span[@title="{TOKEN_CONTACT_KEY}"]'
XPATH_USER = f'//div//div//span//span[@title="{TOKEN_CONTACT_KEY}"]'
