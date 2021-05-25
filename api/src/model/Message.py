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
    key = sap.Column(sap.String(MEDIUM_STRING_SIZE))
    conversationKey = sap.Column(sap.String(MEDIUM_STRING_SIZE))
    ownerKey = sap.Column(sap.String(MEDIUM_STRING_SIZE))
    ownerInfo = sap.Column(sap.String(MEDIUM_STRING_SIZE))

    postedAt = sap.Column(sap.DateTime)
    scannedAt = sap.Column(sap.DateTime)
    createdAt = sap.Column(sap.DateTime)
    updatedAt = sap.Column(sap.DateTime)

    text = sap.Column(sap.String(BIG_STRING_SIZE))

    originalAsText = sap.Column(sap.String(MEDIUM_STRING_SIZE))
    originalAsHtml = sap.Column(sap.String(MEDIUM_STRING_SIZE))

    isPoolerMessage = sap.Column(sap.Boolean)
    poolingStatus = sap.Column(sap.String(LITTLE_STRING_SIZE), default=MessageConstants.DEFAULT_POOLING_STATUS)

    errorCount = sap.Column(sap.Integer(), default=MessageConstants.DEFAULT_ERROR_COUNT)
    errorListAsJson = sap.Column(sap.String(BIG_STRING_SIZE), default=MessageConstants.DEFAULT_ERROR_LIST_AS_JSON)

    def __init__(self,
        id = None,
        key = None,
        conversationKey = None,
        ownerKey = None,
        ownerInfo = None,
        postedAt = None,
        scannedAt = None,
        createdAt = None,
        updatedAt = None,
        text = None,
        originalAsText = None,
        originalAsHtml = None,
        isPoolerMessage = None,
        poolingStatus = None,
        errorCount = None,
        errorListAsJson = None
    ):
        now = DateTimeUtil.dateTimeNow()
        self.id = id
        self.key = getGivenOrDefault(key, getNewErrorId())
        self.ownerKey = getGivenOrDefault(ownerKey, MessageConstants.UNKNOWN_OWNER)
        self.ownerInfo = ownerInfo
        self.conversationKey = conversationKey
        self.postedAt = getGivenOrDefault(DateTimeUtil.forcedlyGetDateTime(postedAt), now)
        self.scannedAt = getGivenOrDefault(DateTimeUtil.forcedlyGetDateTime(scannedAt), now)
        self.createdAt = getGivenOrDefault(DateTimeUtil.forcedlyGetDateTime(createdAt), now)
        self.updatedAt = getGivenOrDefault(DateTimeUtil.forcedlyGetDateTime(updatedAt), now)
        self.text = text
        self.originalAsText = originalAsText
        self.originalAsHtml = originalAsHtml
        self.isPoolerMessage = getGivenOrDefault(isPoolerMessage, MessageConstants.DEFAULT_IS_POOLER_MESSAGE)
        self.poolingStatus = getGivenOrDefault(poolingStatus, MessageConstants.DEFAULT_POOLING_STATUS)
        self.errorCount = getGivenOrDefault(errorCount, MessageConstants.DEFAULT_ERROR_COUNT)
        self.errorListAsJson = errorListAsJson

    def __repr__(self):
        return f'{self.__tablename__}(id: {self.id}, scannedAt: {self.scannedAt}, poolingStatus: {self.poolingStatus} ownerKey: {self.ownerKey}, text: {self.text}, errorCount: {self.errorCount})'
