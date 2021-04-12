import datetime
from python_helper import Constant as c
from python_helper import ObjectHelper, StringHelper, RandomHelper

DEFAULT_DATETIME_PATTERN = '%Y-%m-%d %H:%M:%S'
DEFAULT_DATE_PATTERN = '%Y-%m-%d'
DEFAULT_TIME_PATTERN = '%H:%M:%S'

DATETIME_FULL_PATTERN = '%Y-%m-%d %H:%M:%S.%f'
TIME_FULL_PATTERN = '%H:%M:%S.%f'

PATTERN_LIST = [
    DEFAULT_DATETIME_PATTERN,
    DEFAULT_DATE_PATTERN,
    DEFAULT_TIME_PATTERN,
    DATETIME_FULL_PATTERN,
    TIME_FULL_PATTERN
]

DATETIME_PATTERN_LIST = [
    DEFAULT_DATETIME_PATTERN,
    DATETIME_FULL_PATTERN
]

DATE_PATTERN_LIST = [
    DEFAULT_DATE_PATTERN
]

TIME_PATTERN_LIST = [
    DEFAULT_TIME_PATTERN,
    TIME_FULL_PATTERN
]

DEFAULT_TIME_BEGIN = '00:00:00'
DEFAULT_TIME_END = '23:59:59'

def toString(givenDatetime, pattern=DEFAULT_DATETIME_PATTERN) :
    return givenDatetime if ObjectHelper.isNone(givenDatetime) or isinstance(givenDatetime, str) else parseToString(givenDatetime, pattern=pattern)

def parseToString(given, pattern=DEFAULT_DATETIME_PATTERN) :
    return str(given)

def parseToPattern(given, pattern=DEFAULT_DATETIME_PATTERN, timedelta=False) :
    given = given.strip()
    if StringHelper.isNotBlank(given) :
        parsed = datetime.datetime.strptime(given, pattern)
        if timedelta and pattern in TIME_PATTERN_LIST :
            return datetime.timedelta(hours=parsed.hour, minutes=parsed.minute, seconds=parsed.second, milliseconds=0, microseconds=0)
        if pattern in DATETIME_PATTERN_LIST :
            return parsed
        elif pattern in DATE_PATTERN_LIST :
            return parsed.date()
        elif pattern in TIME_PATTERN_LIST :
            return parsed.time()

def forcedlyParse(given, pattern=DEFAULT_DATETIME_PATTERN, timedelta=False) :
    parsed = None
    for pattern in [pattern] + PATTERN_LIST :
        try :
            parsed = parseToPattern(given, pattern=pattern, timedelta=timedelta)
        except Exception as exception :
            pass
    return parsed

def parseToDateTime(givenDatetime, pattern=DEFAULT_DATETIME_PATTERN) :
    return givenDatetime if ObjectHelper.isNone(givenDatetime) or not isinstance(givenDatetime, str) else parseToPattern(givenDatetime, pattern=pattern)

def forcedlyGetDateTime(givenDatetime, pattern=DEFAULT_DATETIME_PATTERN) :
    return givenDatetime if ObjectHelper.isNone(givenDatetime) or not isinstance(givenDatetime, str) else forcedlyParse(givenDatetime, pattern=pattern)

def forcedlyGetDate(givenDate, pattern=DEFAULT_DATE_PATTERN) :
    return givenDate if ObjectHelper.isNone(givenDate) or not isinstance(givenDate, str) else forcedlyParse(givenDate, pattern=pattern)

def forcedlyGetTime(givenTime, pattern=DEFAULT_TIME_PATTERN) :
    return givenTime if ObjectHelper.isNone(givenTime) or not isinstance(givenTime, str) else forcedlyParse(givenTime, pattern=pattern)

def forcedlyGetInterval(givenTime, pattern=DEFAULT_DATETIME_PATTERN) :
    return givenTime if ObjectHelper.isNone(givenTime) or not isinstance(givenTime, str) else forcedlyParse(givenTime, pattern=pattern, timedelta=True)

def plusSeconds(givenDateTime, seconds=None, deltaInSeconds=None) :
    if ObjectHelper.isNotNone(seconds) :
        deltaInMinutes = datetime.timedelta(seconds=seconds)
    if isinstance(givenDateTime, datetime.time) :
        givenDateTime = forcedlyParse(f'{str(dateNow())} {givenDateTime}')
    return forcedlyGetDateTime(str(givenDateTime)) + deltaInMinutes

def minusSeconds(givenDateTime, seconds=None, deltaInSeconds=None) :
    if ObjectHelper.isNotNone(seconds) :
        deltaInMinutes = datetime.timedelta(seconds=seconds)
    if isinstance(givenDateTime, datetime.time) :
        givenDateTime = forcedlyParse(f'{str(dateNow())} {givenDateTime}')
    return forcedlyGetDateTime(str(givenDateTime)) - deltaInMinutes

def plusMinutes(givenDateTime, minutes=None, deltaInMinutes=None) :
    if ObjectHelper.isNotNone(minutes) :
        deltaInMinutes = datetime.timedelta(seconds=minutes*60)
    if isinstance(givenDateTime, datetime.time) :
        givenDateTime = forcedlyParse(f'{str(dateNow())} {givenDateTime}')
    return forcedlyGetDateTime(str(givenDateTime)) + deltaInMinutes

def minusMinutes(givenDateTime, minutes=None, deltaInMinutes=None) :
    if ObjectHelper.isNotNone(minutes) :
        deltaInMinutes = datetime.timedelta(minutes=minutes)
    if isinstance(givenDateTime, datetime.time) :
        givenDateTime = forcedlyParse(f'{str(dateNow())} {givenDateTime}')
    return forcedlyGetDateTime(str(givenDateTime)) - deltaInMinutes

def plusDays(givenDay, days=None, deltaInDays=None) :
    if ObjectHelper.isNotNone(days) :
        deltaInDays = datetime.timedelta(days=days)
    return forcedlyGetDateTime(str(givenDay)) + deltaInDays

def minusDays(givenDay, days=None, deltaInDays=None) :
    if ObjectHelper.isNotNone(minutes) :
        deltaInDays = datetime.timedelta(days=days)
    return forcedlyGetDateTime(str(givenDay)) - deltaInDays

def getDefaultTimeBegin() :
    return forcedlyGetTime(DEFAULT_TIME_BEGIN)

def getDatetimeMonthBegin() :
    return parseToPattern(c.SPACE.join([c.DASH.join(str(datetime.datetime.now()).split()[0].split(c.DASH)[:-1] + ['01']), DEFAULT_TIME_BEGIN]))

def getDateMonthBeginAndToDateAndTimeMonthBegin() :
    dateMonthBegin = parseToPattern(c.DASH.join(str(datetime.datetime.now()).split()[0].split(c.DASH)[:-1] + ['01']), pattern=DEFAULT_DATE_PATTERN)
    dateToday = dateNow()
    timeMonthBegin = parseToPattern(DEFAULT_TIME_BEGIN, pattern=DEFAULT_TIME_PATTERN)
    return dateMonthBegin, dateToday, timeMonthBegin

def getDatetimeNowMinusMinutesAndNowPlusMinutes(minutes) :
    now = datetime.datetime.now() ###- datetime.datetime.utcnow
    deltaInMinutes = datetime.timedelta(minutes=minutes)
    return minusMinutes(now, deltaInMinutes=deltaInMinutes), plusMinutes(now, deltaInMinutes=deltaInMinutes)

def getTodayDateAndTimeNowMinusMinutesAndTimeNowPlusMinutes(minutes) :
    now = datetime.datetime.now()
    deltaInMinutes = datetime.timedelta(minutes=minutes)
    return now.date(), minusMinutes(now, deltaInMinutes=deltaInMinutes).time(), plusMinutes(now, deltaInMinutes=deltaInMinutes).time()

def getDatetimeFromNowMinusMinutesAndTodayEnd(minutes) :
    now = datetime.datetime.now()
    return minusMinutes(now, minutes=minutes), parseToPattern(c.SPACE.join([str(now).split()[0], DEFAULT_TIME_END]))

def getTodayDateAndFromTimeNowMinusMinutesAndTodayEnd(marginInMinutes=0) :
    now = datetime.datetime.now()
    return now.date(), minusMinutes(now, minutes=marginInMinutes).time(), parseToPattern(DEFAULT_TIME_END, pattern=DEFAULT_TIME_PATTERN)

def dateNow() :
    return datetime.date.today()

def timeNow() :
    return datetime.datetime.now().time()

def dateTimeNow() :
    return datetime.datetime.now()

def of(ofDate=None, ofTime=None) :
    return datetime.datetime.combine(forcedlyGetDate(ofDate), forcedlyGetTime(ofTime))

def date(ofDateTime=None) :
    return ofDateTime.date()

def time(ofDateTime=None) :
    return ofDateTime.time()

def getTodayDateAndTodayTime() :
    ofDateTime = dateTimeNow()
    return date(ofDateTime=ofDateTime), time(ofDateTime=ofDateTime)

def getTodayDateTimeBegin() :
    return parseToDateTime(f'{dateNow()} {DEFAULT_TIME_BEGIN}')

def getTodayDateTimeEnd() :
    return parseToDateTime(f'{dateNow()} {DEFAULT_TIME_END}')

def getWeekDay(ofDatetime=None, ofDate=None, ofTime=None) :
    if ObjectHelper.isNotNone(ofDatetime) :
        return forcedlyGetDateTime(ofDatetime).weekday()
    elif ObjectHelper.isNotNone(ofDate) and ObjectHelper.isNotNone(ofTime) :
        return of(forcedlyGetDate(ofDate), forcedlyGetTime(ofTime)).weekday()
    return datetime.datetime.now().weekday()

def addNoise(givenDatetime) :
    return givenDatetime + datetime.timedelta(milliseconds=RandomHelper.integer(0,999))
