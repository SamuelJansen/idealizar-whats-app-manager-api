from python_helper import ObjectHelper, StringHelper
from python_framework import SqlAlchemyProxy as sap
from ModelAssociation import MESSAGE, MODEL

from sqlalchemy import Boolean

sap.Boolean = Boolean

import MessageConstants

import DateTimeUtil

GIANT_STRING_SIZE = 16384
BIG_STRING_SIZE = 4096
LARGE_STRING_SIZE = 1024
STRING_SIZE = 512
MEDIUM_STRING_SIZE = 128
LITTLE_STRING_SIZE = 64

def getNewErrorId() :
    return f'{MessageConstants.ERROR_ID_STARTS_WITH}{DateTimeUtil.dateTimeNow()}'

def getGivenOrDefault(given, default) :
    return default if ObjectHelper.isNone(given) else given

class Message(MODEL):
    __tablename__ = MESSAGE

    id = sap.Column(sap.Integer(), sap.Sequence(f'{__tablename__}{sap.ID}{sap.SEQ}'), primary_key=True)
    messageId = sap.Column(sap.String(MEDIUM_STRING_SIZE))
    pooledAt = sap.Column(sap.DateTime)
    isPoolerMessage = sap.Column(sap.Boolean)

    owner = sap.Column(sap.String(MEDIUM_STRING_SIZE))
    content = sap.Column(sap.String(BIG_STRING_SIZE))

    ownerContent = sap.Column(sap.String(MEDIUM_STRING_SIZE))
    originalAsText = sap.Column(sap.String(MEDIUM_STRING_SIZE))
    originalAsHtml = sap.Column(sap.String(MEDIUM_STRING_SIZE))

    poolingStatus = sap.Column(sap.String(LITTLE_STRING_SIZE), default=MessageConstants.DEFAULT_POOLING_STATUS)
    errorCount = sap.Column(sap.Integer(), default=MessageConstants.DEFAULT_ERROR_COUNT)
    errorListAsJson = sap.Column(sap.String(BIG_STRING_SIZE), default=MessageConstants.DEFAULT_ERROR_LIST_AS_JSON)

    def __init__(self,
        id = None,
        messageId = None,
        pooledAt = None,
        isPoolerMessage = None,
        owner = None,
        content = None,
        ownerContent = None,
        originalAsText = None,
        originalAsHtml = None,
        poolingStatus = None,
        errorCount = None,
        errorListAsJson = None
    ):
        self.id = id
        self.messageId = getGivenOrDefault(messageId, getNewErrorId())
        self.pooledAt = getGivenOrDefault(DateTimeUtil.forcedlyGetDateTime(pooledAt), DateTimeUtil.dateTimeNow())
        self.isPoolerMessage = getGivenOrDefault(isPoolerMessage, MessageConstants.DEFAULT_IS_POOLER_MESSAGE)
        self.owner = getGivenOrDefault(owner, MessageConstants.UNKNOWN_OWNER)
        self.content = content
        self.ownerContent = ownerContent
        self.originalAsText = originalAsText
        self.originalAsHtml = originalAsHtml
        self.poolingStatus = getGivenOrDefault(poolingStatus, MessageConstants.DEFAULT_POOLING_STATUS)
        self.errorCount = getGivenOrDefault(errorCount, MessageConstants.DEFAULT_ERROR_COUNT)
        self.errorListAsJson = errorListAsJson

    def __repr__(self):
        return f'{self.__tablename__}(id: {self.id}, pooledAt: {self.pooledAt}, poolingStatus: {self.poolingStatus} owner: {self.owner}, content: {self.content}, errorCount: {self.errorCount})'
