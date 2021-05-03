from ContactType import ContactType
from ContactStatus import ContactStatus

class ContactRequestDto :
    def __init__(self,
        key = None,
        type = None,
        name = None
    ) :
        self.key = key
        self.type = ContactType.map(type)
        self.name = name

class ContactResponseDto :
    def __init__(self,
        id = None,
        key = None,
        type = None,
        status = None,
        name = None
    ) :
        self.id = id
        self.key = key
        self.type = ContactType.map(type)
        self.status = ContactStatus.map(status)
        self.name = name
