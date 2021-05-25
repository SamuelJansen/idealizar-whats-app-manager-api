from python_helper import ObjectHelper, StringHelper
from python_framework import ConverterStatic
from python_framework import SqlAlchemyProxy as sap
from ModelAssociation import CONTACT, MODEL

from enumeration.contact import ContactType, ContactStatus
from domain import ContactConstants
from util import DateTimeUtil

GIANT_STRING_SIZE = 16384
BIG_STRING_SIZE = 4096
LARGE_STRING_SIZE = 1024
STRING_SIZE = 512
MEDIUM_STRING_SIZE = 128
LITTLE_STRING_SIZE = 64

class Contact(MODEL):
    __tablename__ = CONTACT

    id = sap.Column(sap.Integer(), sap.Sequence(f'{__tablename__}{sap.ID}{sap.SEQ}'), primary_key=True)
    key = sap.Column(sap.String(MEDIUM_STRING_SIZE), nullable=False)
    createdAt = sap.Column(sap.DateTime, nullable=False)
    updatedAt = sap.Column(sap.DateTime, nullable=False)
    type = sap.Column(sap.String(LITTLE_STRING_SIZE), default=ContactConstants.DEFAULT_TYPE, nullable=False)
    status = sap.Column(sap.String(LITTLE_STRING_SIZE), default=ContactConstants.DEFAULT_STATUS, nullable=False)
    name = sap.Column(sap.String(MEDIUM_STRING_SIZE))

    def __init__(self,
        id = None,
        key = None,
        createdAt = None,
        updatedAt = None,
        type = None,
        status = None,
        name = None
    ):
        now = DateTimeUtil.dateTimeNow()
        self.id = id
        self.key = key
        self.createdAt = ConverterStatic.getValueOrDefault(DateTimeUtil.forcedlyGetDateTime(createdAt), now)
        self.updatedAt = ConverterStatic.getValueOrDefault(DateTimeUtil.forcedlyGetDateTime(updatedAt), now)
        self.type = ConverterStatic.getValueOrDefault(ContactType.ContactType.map(type), ContactConstants.DEFAULT_TYPE)
        self.status = ConverterStatic.getValueOrDefault(ContactStatus.ContactStatus.map(status), ContactConstants.DEFAULT_STATUS)
        self.name = name

    def __repr__(self):
        return f'{self.__tablename__}(id: {self.id}, key: {self.key}, type: {self.type}, name: {self.name})'
