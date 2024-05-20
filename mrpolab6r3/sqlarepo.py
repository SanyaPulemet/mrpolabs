from abc import ABC, abstractmethod
from sqlalchemy.orm import relationship, declarative_base, sessionmaker, Session


class AbstractRepository(ABC):

    @abstractmethod
    def create(self, entity):
        raise NotImplementedError()

    @abstractmethod
    def get(self, id):
        raise NotImplementedError()

    @abstractmethod
    def list(self):
        raise NotImplementedError()

    @abstractmethod
    def update(self, entity):
        raise NotImplementedError()

    @abstractmethod
    def delete(self, entity):
        raise NotImplementedError()


class SQLAlchemyRepository(AbstractRepository):

    def __init__(self, session: Session, model_class):
        self.session = session
        self.model_class = model_class

    def create(self, entity):
        self.session.add(entity)
        self.session.commit()
        return entity

    def get(self, id):
        return self.session.query(self.model_class).filter_by(id=id).one_or_none()

    def list(self):
        query = self.session.query(self.model_class)
        return query.all()

    def update(self, entity):
        obj = self.get(entity.id)
        if obj:
            for key, value in vars(entity).items():
                setattr(obj, key, value)
            self.session.commit()
            return obj
        return None

    def delete(self, entity):
        obj = self.get(entity.id)
        if obj:
            self.session.delete(obj)
            self.session.commit()
            return True
        return False