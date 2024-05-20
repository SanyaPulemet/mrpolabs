import unittest
from datetime import timedelta
from classes import *
from services import BusinessRules


class TestBusinessRules(unittest.TestCase):
    def setUp(self):
        self.service = BusinessRules()

    def test_make_order(self):
        user = Client(1, 'name', 'phone', [], [])
        delivery_address = "test address"
        items = [Burger(1, "borgar"), BurgerSet(1, "borgars", [Burger(1, "borgar"), Burger(1, "borgar")])]

        order = self.service.make_order(user, delivery_address, items)
        # что проверить??? теперь буду проверять не вызов функции а верную отработку?.. пусть хоть так
        self.assertEqual(order.client.id, user.id)

    def test_mark_order_as_taken(self):  # соответствует ли id курьера ожидаемому
        order_id = 1
        courier_id = 2
        client = Client(1, "client", "312", [], [])
        courier = Courier(courier_id, "courier", [])
        items = [Burger(1, "borgar"), BurgerSet(1, "borgars", [Burger(1, "borgar"), Burger(1, "borgar")])]
        test_order = Order(order_id, client, datetime.now(), None,
                           "address", None, items,
                           sum(300 if isinstance(item, Burger) else 800 for item in items))

        self.service.mark_order_as_taken(test_order, courier)
        self.assertEqual(test_order.courier.id, courier_id)

    def test_mark_order_as_delivered(self):  # дата установлена
        client = Client(1, "client", "3123", [], [])
        courier = Courier(1, "courier", [])
        items = [Burger(1, "borgar"), BurgerSet(1, "borgars", [Burger(1, "borgar"), Burger(1, "borgar")])]
        test_order = Order(1, client, datetime.now(), None,
                           "address", courier, items,
                           sum(300 if isinstance(item, Burger) else 800 for item in items))

        self.service.mark_order_as_delivered(test_order, courier)
        self.assertIsNotNone(test_order.delivery_time)

    def test_leave_comment(self):
        client = Client(1, "client", "3123", [], [])
        courier = Courier(1, "courier", [])
        items = [Burger(1, "borgar"), BurgerSet(1, "borgars", [Burger(1, "borgar"), Burger(1, "borgar")])]
        test_order = Order(1, client, datetime.now(), None,
                           "address", courier, items,
                           sum(300 if isinstance(item, Burger) else 800 for item in items))
        comment_text = "comment"

        comment = self.service.leave_comment(test_order, client, comment_text)
        # что проверить??? теперь буду проверять не вызов функции а верную отработку?.. пусть хоть так
        self.assertEqual(comment.text, comment_text)

    def test_check_delivery_time(self):  # цена уменьшилась
        client = Client(1, "client", "3123", [], [])
        courier = Courier(1, "courier", [])
        items = [Burger(1, "borgar"), BurgerSet(1, "borgars", [Burger(1, "borgar"), Burger(1, "borgar")])]

        creation_time = datetime.now() - timedelta(hours=3)
        delivery_time = datetime.now()

        test_order = Order(1, client, creation_time, delivery_time,
                           "address", courier, items,
                           sum(300 if isinstance(item, Burger) else 800 for item in items))

        self.service.check_delivery_time(test_order)
        self.assertEqual(test_order.price, sum(300 if isinstance(item, Burger) else 800 for item in items) // 2)
