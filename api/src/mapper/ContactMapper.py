from python_helper import DateTimeHelper
from python_framework import Mapper, MapperMethod, ConverterStatic
from model import Contact
from dto import ContactDto

@Mapper()
class ContactMapper:

    @MapperMethod(requestClass=[ContactDto.ContactRequestDto], responseClass=[Contact.Contact])
    def fromRequestDtoToModel(self, dto, model) :
        self.overrideDateData(model)
        return model

    @MapperMethod(requestClass=[[ContactDto.ContactRequestDto]], responseClass=[[Contact.Contact]])
    def fromRequestDtoListToModelList(self, dtoList, modelList) :
        for model in modelList :
            self.overrideDateData(model)
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
    def overrideModelValuesFromRequestDto(self, model, dto, status=None) :
        model.type = dto.type
        model.status = ConverterStatic.getValueOrDefault(status, model.status)
        model.name = dto.name
        self.overrideDateData(model)

    @MapperMethod(requestClass=[Contact.Contact])
    def overrideDateData(self, model) :
        now = DateTimeHelper.dateTimeNow()
        model.createdAt = ConverterStatic.getValueOrDefault(model.createdAt, now)
        model.updatedAt = now
