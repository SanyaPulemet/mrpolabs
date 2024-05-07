from datetime import datetime, timedelta
from classes import *


class BusinessRules:
    def make_order(self, user: Client, delivery_address, items):
        order = Order(user,
                      datetime.now(),
                      None,
                      delivery_address,
                      None,
                      items,
                      sum(300 if isinstance(item, Burger) else 800 for item in items))
        return order

    def mark_order_as_taken(self, order: Order, courier: Courier):
        if not order.courier:
            order.courier = courier
            return True
        return False

    def mark_order_as_delivered(self,  order: Order, courier: Courier):
        if order.courier and order.courier == courier:
            order.delivery_time = datetime.now()
            self.check_delivery_time(order)
            return True
        return False

    def leave_comment(self, order: Order,  user: Client, comment_text):
        comment = Comment(comment_text, user,
                          order)
        return comment

    def check_delivery_time(self, order: Order):
        if order.delivery_time and order.creation_time and (abs(order.delivery_time - order.creation_time) > timedelta(hours=2)):
            order.price = order.price // 2
