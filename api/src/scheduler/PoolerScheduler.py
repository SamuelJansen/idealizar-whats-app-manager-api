from python_helper import log
from python_framework import Scheduler, SchedulerMethod, SchedulerType

import PoolerConstants

@Scheduler()
class PoolerScheduler :

    @SchedulerMethod(SchedulerType.INTERVAL, seconds=PoolerConstants.SCHEDULE_POOL_INTERVAL_IN_SECONDS, instancesUpTo=2)
    def whatsAppPooler(self) :
        # log.debug(self.whatsAppPooler, 'starded')
        # self.service.pooler.inteigentLoop()
        # log.debug(self.whatsAppPooler, 'ended')
        ...
