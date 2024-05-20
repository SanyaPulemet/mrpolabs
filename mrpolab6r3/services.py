from datetime import datetime, timedelta
from sqla import *
from classes import *


async def make_order(user, delivery_address, items):
    if type(user) == ClientDB:
        order = OrderDB()
        order.client = user.id
        order.creation_time = datetime.now()
        order.delivery_address = delivery_address
        return order
    order = Order(user,
                  datetime.now(),
                  None,
                  delivery_address,
                  None,
                  items,
                  sum(300 if isinstance(item, Burger) else 800 for item in items))
    return order


async def mark_order_as_taken(order, courier):
    if not order.courier:
        order.courier = courier.id
        return True
    return False


async def mark_order_as_delivered(order, courier):
    if order.courier and order.courier == courier.id:
        order.delivery_time = datetime.now()
        return True
    return False


async def leave_comment(order, user, comment_text):
    if type(user) == ClientDB:
        comment = CommentDB()
        comment.text = comment_text
        return comment
    comment = Comment(comment_text, user,
                      order)
    return comment


async def check_delivery_time(order: Order):
    if order.delivery_time and order.creation_time and (
            abs(order.delivery_time - order.creation_time) > timedelta(hours=2)):
        order.price = order.price // 2
        return True
    return False