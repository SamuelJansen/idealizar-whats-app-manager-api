from python_helper import ObjectHelper
from python_framework import SqlAlchemyProxy as sap
from python_framework import Repository
import Message

@Repository(model = Message.Message)
class MessageRepository:

    def findAll(self) :
        return self.repository.findAllAndCommit(self.model)

    def existsById(self, id) :
        return self.repository.existsByIdAndCommit(id, self.model)

    def findById(self, id) :
        if self.existsById(id) :
            return self.repository.findByIdAndCommit(id, self.model)

    def existsByKey(self, key) :
        return self.repository.existsByKeyAndCommit(key, self.model)

    def findByKey(self, key) :
        if self.existsByKey(key) :
            return self.repository.findByKeyAndCommit(key, self.model)

    def notExistsById(self, id) :
        return not self.existsById(id)

    def save(self, model) :
        return self.repository.saveAndCommit(model)

    def saveAll(self, modelList):
        return self.repository.saveAllAndCommit(modelList)

    def deleteById(self, id):
        self.repository.deleteByIdAndCommit(id, self.model)

    def findAllKeyIdIn(self, keyList) :
        modelList = self.repository.session.query(self.model).filter(self.model.key.in_(keyList)).all()
        self.repository.session.commit()
        return modelList

    def existsConversation(self, conversationKey) :
        objectExists = self.repository.session.query(sap.exists().where(self.model.conversationKey == conversationKey)).one()[0]
        self.repository.session.commit()
        return objectExists

    def findLastMessageKey(self, conversationKey) :
        model = self.repository.session.query(self.model.key).filter(
            self.model.conversationKey == conversationKey
        ).order_by(self.model.postedAt.desc()).first()[0]
        self.repository.session.commit()
        return model
