from python_helper import log
from python_framework import Scheduler, SchedulerMethod, SchedulerType

@Scheduler()
class CallScheduler :

    @SchedulerMethod(SchedulerType.INTERVAL, minutes=1, instancesUpTo=2)
    def openPresentCall(self) :
        log.debug(self.openPresentCall, 'starded')
        try :
            self.service.conversation.checkAndInform()
        except Exception as exception :
            log.error(self.openPresentCall, 'Error at scheduler', exception)
        log.debug(self.openPresentCall, 'ended')
