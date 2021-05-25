from python_helper import ObjectHelper
from python_framework import SqlAlchemyProxy as sap
from python_framework import Repository
from model import Contact

@Repository(model = Contact.Contact)
class ContactRepository:

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

    def findAllByIdIn(self, idList) :
        modelList = self.repository.session.query(self.model).filter(self.model.id.in_(idList)).all()
        self.repository.session.commit()
        return modelList

    def existsByKeyAndByTypeAndByStatus(self, key, modelType, modelStatus) :
        objectExists = self.repository.session.query(
            sap.exists().where(
                sap.and_(
                    self.model.key == key,
                    sap.and_(
                        self.model.type == modelType,
                        self.model.status == modelStatus
                    )
                )

            )
        ).one()[0]
        self.repository.session.commit()
        return objectExists

    def findByKeyAndByStatus(self, key, modelStatus) :
        model = self.repository.session.query(self.model).filter(
            sap.and_(
                self.model.key == key,
                self.model.status == modelStatus
            )
        ).first()
        self.repository.session.commit()
        return model

    def findAllByKeyIn(self, keyList) :
        featureList = self.repository.session.query(self.model).filter(self.model.key.in_(keyList)).all()
        self.repository.session.commit()
        return featureList
