from ContactType import ContactType

class ContactPoolerRequestDto :
    def __init__(self,
        key = None,
        type = None
    ) :
        self.key = key
        self.type = ContactType.map(type)
