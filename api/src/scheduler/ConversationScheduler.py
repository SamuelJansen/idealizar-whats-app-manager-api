from python_helper import log
from python_framework import Scheduler, SchedulerMethod, SchedulerType

from domain import ConversationConstants

@Scheduler()
class ConversationScheduler :

    @SchedulerMethod(SchedulerType.INTERVAL, seconds=ConversationConstants.SCHEDULER_INTERVAL_IN_SECONDS, instancesUpTo=ConversationConstants.SCHEDULER_MAX_SIMULTANEOUS_INSTANCES)
    def inteligentLoop(self) :
        log.debug(self.inteligentLoop, 'starded')
        try :
            self.service.conversation.inteligentLoop()
        except Exception as exception :
            log.error(self.inteligentLoop, 'Error at scheduler', exception)
        log.debug(self.inteligentLoop, 'ended')
