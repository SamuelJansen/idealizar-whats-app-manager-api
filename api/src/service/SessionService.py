from python_framework import Service, ServiceMethod

import Session

@Service()
class SessionService:

    @ServiceMethod(requestClass=[Session.Session])
    def create(self, model) :
        return self.repository.message.save(model)

    @ServiceMethod()
    def findMostRecent(self) :
        return self.repository.session.findMostRecentUpdatedAt()
