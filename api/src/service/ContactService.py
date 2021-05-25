from python_framework import Service, ServiceMethod

from ContactStatus import ContactStatus

from model import Contact
from dto import ContactDto

@Service()
class ContactService :

    @ServiceMethod()
    def findAll(self) :
        modelList = self.repository.contact.findAll()
        return self.mapper.contact.fromModelListToResponseDtoList(modelList)

    @ServiceMethod(requestClass=[ContactDto.ContactRequestDto])
    def safellyCreateOrUpdate(self, dto) :
        if not self.exists(dto) :
            model = self.create(dto)
        else :
            model = self.update(dto)
        return self.mapper.contact.fromModelToResponseDto(model)

    @ServiceMethod(requestClass=[[ContactDto.ContactRequestDto]])
    def safellyCreateOrUpdateAll(self, dtoList) :
        dtoResponseList = []
        for dto in dtoList :
            dtoResponseList.append(self.safellyCreateOrUpdate(dto))
        return dtoResponseList

    @ServiceMethod(requestClass=[ContactDto.ContactRequestDto])
    def create(self, dto) :
        model = self.mapper.contact.fromRequestDtoToModel(dto)
        model.status = ContactStatus.ACTIVE
        return self.repository.contact.save(model)

    @ServiceMethod(requestClass=[ContactDto.ContactRequestDto])
    def update(self, dto) :
        model = self.repository.contact.findByKeyAndByStatus(dto.key, ContactStatus.ACTIVE)
        self.mapper.contact.overrideModelValuesFromRequestDto(model, dto)
        return self.repository.contact.save(model)

    @ServiceMethod(requestClass=[ContactDto.ContactRequestDto])
    def exists(self, dto) :
        return self.repository.contact.existsByKeyAndByTypeAndByStatus(dto.key, dto.type, ContactStatus.ACTIVE)
