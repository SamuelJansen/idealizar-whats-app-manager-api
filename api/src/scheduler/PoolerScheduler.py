from python_helper import log
from SchedulerAnnotation import Scheduler, SchedulerMethod

import PoolerConstants

@Scheduler()
class PoolerScheduler :

    @SchedulerMethod('interval', seconds=PoolerConstants.SCHEDULE_POOL_INTERVAL_IN_SECONDS, max_instances=2)
    # @SchedulerMethod('interval', seconds=10, max_instances=2)
    def whatsAppPooler(self) :
        # log.debug(self.whatsAppPooler, 'starded')
        self.service.pooler.inteigentLoop()
        # log.debug(self.whatsAppPooler, 'ended')
        ...
