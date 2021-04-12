from python_helper import ObjectHelper, StringHelper
from python_framework import SqlAlchemyProxy as sap
from ModelAssociation import SESSION, MODEL

import DateTimeUtil

GIANT_STRING_SIZE = 16384
BIG_STRING_SIZE = 4096
LARGE_STRING_SIZE = 1024
STRING_SIZE = 512
MEDIUM_STRING_SIZE = 128
LITTLE_STRING_SIZE = 64

def getGivenOrDefault(given, default) :
    return default if ObjectHelper.isNone(given) else given
    
class Session(MODEL):
    __tablename__ = SESSION

    id = sap.Column(sap.Integer(), sap.Sequence(f'{__tablename__}{sap.ID}{sap.SEQ}'), primary_key=True)
    updatedAt = sap.Column(sap.DateTime)
    sessionId = sap.Column(sap.String(MEDIUM_STRING_SIZE))
    commandExecutor = sap.Column(sap.String(MEDIUM_STRING_SIZE))

    def __init__(self,
        id = None,
        updatedAt = None,
        sessionId = None,
        commandExecutor = None
    ):
        self.id = id
        self.updatedAt = getGivenOrDefault(DateTimeUtil.forcedlyGetDateTime(updatedAt), DateTimeUtil.dateTimeNow())
        self.sessionId = sessionId
        self.commandExecutor = commandExecutor

    def __repr__(self):
        return f'{self.__tablename__}(id: {self.id}, updatedAt: {self.updatedAt}, sessionId: {self.sessionId} commandExecutor: {self.commandExecutor})'
