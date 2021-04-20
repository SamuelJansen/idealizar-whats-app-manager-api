from python_framework import Mapper, MapperMethod
import Contact, ContactDto

@Mapper()
class ContactMapper:

    @MapperMethod(requestClass=[ContactDto.ContactRequestDto], responseClass=[Contact.Contact])
    def fromRequestDtoToModel(self, dto, model) :
        return model

    @MapperMethod(requestClass=[[ContactDto.ContactRequestDto]], responseClass=[[Contact.Contact]])
    def fromRequestDtoListToModelList(self, dtoList, modelList) :
        return modelList

    @MapperMethod(requestClass=[Contact.Contact], responseClass=[ContactDto.ContactResponseDto])
    def fromModelToResponseDto(self, model, dto) :
        return dto

    @MapperMethod(requestClass=[[Contact.Contact]], responseClass=[[ContactDto.ContactResponseDto]])
    def fromModelListToResponseDtoList(self, modelList, dtoList) :
        return dtoList

    @MapperMethod(requestClass=[Contact.Contact], responseClass=[ContactDto.ContactRequestDto])
    def fromModelToRequestDto(self, model, dto) :
        return dto

    @MapperMethod(requestClass=[[Contact.Contact]], responseClass=[[ContactDto.ContactRequestDto]])
    def fromModelListToRequestDtoList(self, modelList, dtoList) :
        return dtoList

    @MapperMethod(requestClass=[Contact.Contact, ContactDto.ContactResponseDto])
    def overrideModelValuesFromRequestDto(self, model, dto) :
        self.updatedAt = getGivenOrDefault(DateTimeUtil.forcedlyGetDateTime(updatedAt), DateTimeUtil.dateTimeNow())
        model.type = dto.type
        model.status = dto.status
        model.name = dto.name
