from sqlalchemy import create_engine, Column, String, ForeignKey, Integer, DateTime
from sqlalchemy.orm import relationship, declarative_base, sessionmaker, Session
from abc import ABC, abstractmethod


# это было ошибкой не раскидать файлы по папкам >~<


Base = declarative_base()


class Burger(Base):
    __tablename__ = 'burgers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)

    burger_sets = relationship("BurgerSet", secondary="burger_set_association",back_populates="burgers")
    orders = relationship("Order", secondary='order_burger_association', back_populates="burgers")


class BurgerSet(Base):
    __tablename__ = 'burger_sets'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)

    burgers = relationship("Burger", secondary="burger_set_association", back_populates="burger_sets")
    orders = relationship("Order", secondary='order_burgerset_association', back_populates="burgersets")


class BurgerSetAssociation(Base):
    __tablename__ = 'burger_set_association'

    burger_id = Column(Integer, ForeignKey('burgers.id'), primary_key=True)
    burger_set_id = Column(Integer, ForeignKey('burger_sets.id'), primary_key=True)


class Courier(Base):
    __tablename__ = 'couriers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)

    orders = relationship("Order", back_populates="courier")


class Client(Base):
    __tablename__ = 'clients'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    phone = Column(String)

    orders = relationship("Order", back_populates="client")
    comments = relationship("Comment", back_populates="client")


class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, autoincrement=True)
    creation_time = Column(DateTime)
    delivery_time = Column(DateTime)
    delivery_address = Column(String)
    price = Column(Integer)
    courier_id = Column(Integer, ForeignKey('couriers.id'))
    client_id = Column(Integer, ForeignKey('clients.id'))
    comment_id = Column(Integer, ForeignKey('comments.id'))

    courier = relationship("Courier", back_populates="orders")
    client = relationship("Client", back_populates="orders")
    comment = relationship("Comment", back_populates="order")
    burgers = relationship("Burger", secondary='order_burger_association', back_populates="orders")
    burgersets = relationship("BurgerSet", secondary='order_burgerset_association', back_populates="orders")


class OrderBurgerAssociation(Base):
    __tablename__ = 'order_burger_association'

    order_id = Column(Integer, ForeignKey('orders.id'), primary_key=True)
    burger_id = Column(Integer, ForeignKey('burgers.id'), primary_key=True)


class OrderBurgerSetAssociation(Base):
    __tablename__ = 'order_burgerset_association'

    order_id = Column(Integer, ForeignKey('orders.id'), primary_key=True)
    burgerset_id = Column(Integer, ForeignKey('burger_sets.id'), primary_key=True)


class Comment(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(String)
    client_id = Column(Integer, ForeignKey('clients.id'))

    order = relationship("Order", back_populates="comment")
    client = relationship("Client", back_populates="comments")


#engine = create_engine('sqlite:///example.db', echo=True)
'''engine = create_engine('sqlite:///:memory:')
Base.metadata.create_all(engine)

session = sessionmaker(bind=engine)()'''


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


'''burger_repository = SQLAlchemyRepository(session, Burger)
order_repository = SQLAlchemyRepository(session, Order)

new_burger = Burger(name='Cheeseburger')
new_burger2 = Burger(name='Cheeseburger')
burger_repository.create(new_burger)
burger_repository.create(new_burger2)

all_burgers = burger_repository.list()
print(all_burgers)

burger_to_update = burger_repository.get(new_burger.id)
burger_to_update.name = 'Veggie Burger'
burger_repository.update(burger_to_update)

burger_repository.delete(burger_to_update)

new_order = Order()
print(new_order.burgers)
order_repository.create(new_order)

all_burgers = burger_repository.list()
for burger in all_burgers:
    new_order.burgers.append(burger)

order_repository.update(new_order)
print(new_order.burgers)

print(all_burgers)
print(order_repository.list())

session.close()'''