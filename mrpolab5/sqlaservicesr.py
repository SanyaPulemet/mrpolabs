from datetime import datetime, timedelta

import services
from classes import *
from sqla import *
import sqla
from services import *


class BusinessRules:
    rules = services.BusinessRules()
    def make_order(self, user: int, delivery_address, items, user_repo, order_repo):
        user = user_repo.get(user)
        order = rules.make_order(user, delivery_address, items)
        sqlalchemy_order = Order(
            creation_time=order.creation_time,
            delivery_time=order.delivery_time,
            delivery_address=order.delivery_address,
            price=order.price,
            client_id=order.client.id if order.client is not None else None,
            courier_id=order.courier.id if order.courier is not None else None,
        )
        return order_repo.create(sqlalchemy_order)

    def mark_order_as_taken(self, order: int, courier: int, order_repo, courier_repo):
        order = order_repo.get(order)
        if not order.courier:
            order.courier = courier_repo.get(courier)
            print(courier_repo.get(courier))
            return True
        return False

    def mark_order_as_delivered(self,  order1: int, courier: int, order_repo, courier_repo):
        order = order_repo.get(order1)
        courier = courier_repo.get(courier)
        if order.courier and order.courier == courier:
            order.delivery_time = datetime.now()
            print(order.delivery_time)
            self.check_delivery_time(order1, order_repo)
            return True
        return False

    def leave_comment(self, comment_text, comment_repo):
        comment = sqla.Comment(text=comment_text)
        comment_repo.create(comment)
        return comment

    def check_delivery_time(self, order: int, order_repo):
        order = order_repo.get(order)
        if order.delivery_time and order.creation_time and (abs(order.delivery_time - order.creation_time) > timedelta(hours=2)):
            order.price = order.price // 2
            print(order.price)
        return


engine = create_engine('sqlite:///:memory:')
Base.metadata.create_all(engine)

session = sessionmaker(bind=engine)()

rules = BusinessRules()

#burger_repository = SQLAlchemyRepository(session, Burger)
order_repository = SQLAlchemyRepository(session, Order)
client_repository = SQLAlchemyRepository(session, Client) # почему я зову его юзером?
comment_repository = SQLAlchemyRepository(session, Comment)
courier_repository = SQLAlchemyRepository(session, Courier)

client1 = sqla.Client(name='user1')
client_repository.create(client1)
client2 = sqla.Client(name='user2')
client_repository.create(client2)

'''courier1 = Courier(name='courier1')
courier_repository.create(courier1)
courier2 = Courier(name='courier2')
courier_repository.create(courier2)'''

order1 = sqla.Order(creation_time=datetime(year=2024, month=5, day=1), price=1000)
order_repository.create(order1)

print(rules.make_order(client1.id, "test", [], client_repository, order_repository).delivery_address)

'''rules.mark_order_as_taken(order1.id, courier1.id, order_repository, courier_repository)

rules.mark_order_as_delivered(order1.id, courier1.id, order_repository, courier_repository) # проверяет и 5, вложенность

print(rules.leave_comment("txt", comment_repository).text)'''

#rules.make_order(client1.id)

'''new_burger = Burger(name='Cheeseburger')
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
print(order_repository.list())'''

session.close()