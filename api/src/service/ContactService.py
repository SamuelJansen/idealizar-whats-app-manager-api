from python_framework import Service, ServiceMethod

import ContactDto

@Service()
class ContactService :

    @ServiceMethod(requestClass=[ContactDto.ContactPoolerRequestDto])
    def exists(self, dto) :
        return self.repository.contact.existsByKeyAndByType(dto.key, dto.type)
