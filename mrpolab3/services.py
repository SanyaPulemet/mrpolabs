from datetime import datetime, timedelta
from repositories import *
from classes import *


class BusinessRules:
    def __init__(self, client_repository: ClientRepository, courier_repository: CourierRepository,
                 orders_repository: OrdersRepository, comments_repository: CommentsRepository):
        self.client_repository = client_repository
        self.courier_repository = courier_repository
        self.order_repository = orders_repository
        self.comment_repository = comments_repository

    def make_order(self, user_id, delivery_address, items):
        order = Order(len(self.order_repository.orders),
                      self.client_repository.find_by_id(user_id),
                      datetime.now(),
                      None,
                      delivery_address,
                      None,
                      items,
                      sum(300 if isinstance(item, Burger) else 800 for item in items))
        self.order_repository.add_order(order)

    def mark_order_as_taken(self, order_id, courier_id):
        order = self.order_repository.find_by_id(order_id)
        if not order.courier:
            order.courier = self.courier_repository.find_by_id(courier_id)

    def mark_order_as_delivered(self, order_id, courier_id):
        order = self.order_repository.find_by_id(order_id)
        if order.courier.id and order.courier.id == courier_id:
            order.delivery_time = datetime.now()
            self.check_delivery_time(order_id)

    def leave_comment(self, order_id, user_id, comment_text):
        comment = Comment(len(self.comment_repository.comments),
                          comment_text, self.client_repository.find_by_id(user_id),
                          self.order_repository.find_by_id(order_id))
        self.comment_repository.add_comment(comment)

    def check_delivery_time(self, order_id):
        order = self.order_repository.find_by_id(order_id)
        if order.delivery_time and (abs(order.delivery_time - order.creation_time) > timedelta(hours=2)):
            order.price = order.price // 2
