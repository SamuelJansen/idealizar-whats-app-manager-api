from python_helper import ObjectHelper
from python_framework import ConverterStatic, Serializer
from domain import MessageConstants
from dto import MessageScanDto, MessageWriteDto

def getLastOwner(lastOwner) :
    return ConverterStatic.getValueOrDefault(lastOwner, MessageConstants.UNKNOWN_OWNER)

def toReadResponseDtoList(messageList) :
    if ObjectHelper.isNotNone(messageList) :
        return Serializer.convertFromObjectToObject(messageList, [[MessageScanDto.MessageScanResponseDto]])
    return MessageConstants.EMPTY_MESSAGE_LIST

def toReadResponseDto(message) :
    if ObjectHelper.isNotNone(message) :
        return Serializer.convertFromObjectToObject(message, [MessageScanDto.MessageScanResponseDto])
    return message

def toWriteRequestDtoList(messageList) :
    if ObjectHelper.isNotNone(messageList) :
        return Serializer.convertFromObjectToObject(messageList, [[MessageWriteDto.MessageWriteRequestDto]])
    return MessageConstants.EMPTY_MESSAGE_LIST

def toWriteRequestDto(message) :
    if ObjectHelper.isNotNone(message) :
        return Serializer.convertFromObjectToObject(message, [MessageWriteDto.MessageWriteRequestDto])
    return message

def toWriteResponseDtoList(messageList) :
    if ObjectHelper.isNotNone(messageList) :
        return Serializer.convertFromObjectToObject(messageList, [[MessageWriteDto.MessageWriteResponseDto]])
    return MessageConstants.EMPTY_MESSAGE_LIST
