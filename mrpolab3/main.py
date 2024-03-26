from datetime import datetime
from classes import *
from repositories import *


client1 = Client(1, 'client1', 'clientphone1')
client2 = Client(2, 'client2', 'clientphone2')

burger = Burger(1, 'borgar')
borgarList = []
borgarList.append(burger)
burgerSet = BurgerSet(1, 'borgarset', borgarList)

courier1 = Courier(1, 'courier1')
courier2 = Courier(2, 'courier2')

order1 = Order(1, client1, datetime.now(), datetime.now(), 'address1', courier1, [burgerSet, burger], 12413312312)
order2 = Order(2, client2, datetime.now(), datetime.now(), 'address2', courier2, [burgerSet, burger], 12413312311)

comment1 = Comment(1, 'нормальнг', client1, order1)
comment2 = Comment(2, 'нормальнге', client2, order2)


clientRepository = ClientRepository()
clientRepository.add_client(client1)
clientRepository.add_client(client2)

ordersRepository = OrdersRepository()
ordersRepository.add_order(order1)
ordersRepository.add_order(order2)

commentsRepository = CommentsRepository()
commentsRepository.add_comment(comment1)
commentsRepository.add_comment(comment2)

clientRepository.get_all_clients()
ordersRepository.get_all_orders()
commentsRepository.get_all_comments()

