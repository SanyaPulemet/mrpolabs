from sqlalchemy import create_engine, Column, String, ForeignKey, Integer, DateTime
from sqlalchemy.orm import relationship, declarative_base, sessionmaker, Session
from typing import Dict, Any
from datetime import *
from decimal import Decimal


# это было ошибкой не раскидать файлы по папкам >~<


Base = declarative_base()


class BurgerDB(Base):
    __tablename__ = 'burgers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)

    burger_sets = relationship("BurgerSetDB", secondary="burger_set_association",back_populates="burgers")
    orders = relationship("OrderDB", secondary='order_burger_association', back_populates="burgers")


class BurgerSetDB(Base):
    __tablename__ = 'burger_sets'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)

    burgers = relationship("BurgerDB", secondary="burger_set_association", back_populates="burger_sets")
    orders = relationship("OrderDB", secondary='order_burgerset_association', back_populates="burgersets")


class BurgerSetAssociation(Base):
    __tablename__ = 'burger_set_association'

    burger_id = Column(Integer, ForeignKey('burgers.id'), primary_key=True)
    burger_set_id = Column(Integer, ForeignKey('burger_sets.id'), primary_key=True)


class CourierDB(Base):
    __tablename__ = 'couriers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)

    orders = relationship("OrderDB", back_populates="courier_r")

    @property
    def JSONify(self):
        dictionary = {
            'id': self.id,
            'name': self.name,
            }

        return toJSONable(dictionary)


class ClientDB(Base):
    __tablename__ = 'clients'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))
    phone = Column(String(255))

    orders = relationship("OrderDB", back_populates="client_r")
    comments = relationship("CommentDB", back_populates="client_r")

    @property
    def JSONify(self):
        dictionary = {
            'id': self.id,
            'name': self.name,
            'phone': self.phone,
            }

        return toJSONable(dictionary)


class OrderDB(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, autoincrement=True)
    creation_time = Column(DateTime)
    delivery_time = Column(DateTime)
    delivery_address = Column(String(255))
    price = Column(Integer)
    courier = Column(Integer, ForeignKey('couriers.id'))
    client = Column(Integer, ForeignKey('clients.id'))
    comment = Column(Integer, ForeignKey('comments.id'))

    courier_r = relationship("CourierDB", back_populates="orders")
    client_r = relationship("ClientDB", back_populates="orders")
    comment_r = relationship("CommentDB", back_populates="order")
    burgers = relationship("BurgerDB", secondary='order_burger_association', back_populates="orders")
    burgersets = relationship("BurgerSetDB", secondary='order_burgerset_association', back_populates="orders")

    @property
    def JSONify(self):
        dictionary = {
            'id': self.id,
            'creation_time': self.creation_time,
            'delivery_time': self.delivery_time,
            'delivery_address': self.delivery_address,
            'price': self.price,
            'courier': self.courier,
            'client': self.client,
            'comment': self.comment,
            }

        return toJSONable(dictionary)


class OrderBurgerAssociation(Base):
    __tablename__ = 'order_burger_association'

    order_id = Column(Integer, ForeignKey('orders.id'), primary_key=True)
    burger_id = Column(Integer, ForeignKey('burgers.id'), primary_key=True)


class OrderBurgerSetAssociation(Base):
    __tablename__ = 'order_burgerset_association'

    order_id = Column(Integer, ForeignKey('orders.id'), primary_key=True)
    burgerset_id = Column(Integer, ForeignKey('burger_sets.id'), primary_key=True)


class CommentDB(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(String(255))
    client = Column(Integer, ForeignKey('clients.id'))

    order = relationship("OrderDB", back_populates="comment_r")
    client_r = relationship("ClientDB", back_populates="comments")

    @property
    def JSONify(self):
        dictionary = {
            'id': self.id,
            'text': self.text,
            'client': self.client,
        }

        return toJSONable(dictionary)


#engine = create_engine('sqlite:///example.db', echo=True)
'''engine = create_engine('sqlite:///:memory:')
Base.metadata.create_all(engine)

session = sessionmaker(bind=engine)()'''

'''
engine = create_engine('sqlite:///:memory:')
Base.metadata.create_all(engine)
session = sessionmaker(bind=engine)()

burger_repository = SQLAlchemyRepository(session, BurgerDB)
order_repository = SQLAlchemyRepository(session, OrderDB)

new_burger = BurgerDB(name='Cheeseburger')
new_burger2 = BurgerDB(name='Cheeseburger')
burger_repository.create(new_burger)
burger_repository.create(new_burger2)

all_burgers = burger_repository.list()
print(all_burgers)

burger_to_update = burger_repository.get(new_burger.id)
burger_to_update.name = 'Veggie BurgerDB'
burger_repository.update(burger_to_update)

burger_repository.delete(burger_to_update)

new_order = OrderDB()
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

def toJSONable(dictionary: Dict[str, Any]) -> Dict[str, Any]:
    for key, value in dictionary.items():
        if isinstance(value, (datetime, time, date)):
            dictionary[key] = str(value)
        if isinstance(value, Decimal):
            dictionary[key] = float(value)

    return dictionary