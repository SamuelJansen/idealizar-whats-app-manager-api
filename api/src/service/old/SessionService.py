from python_framework import Service, ServiceMethod

import Session

@Service()
class SessionService:

    @ServiceMethod(requestClass=[str, str])
    def create(self, sessionId, commandExecutor) :
        return self.repository.session.save(
            Session.Session(sessionId=sessionId, commandExecutor=commandExecutor)
        )

    @ServiceMethod()
    def findMostRecent(self) :
        return self.repository.session.findMostRecentUpdatedAt()
