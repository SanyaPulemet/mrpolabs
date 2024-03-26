import unittest
from datetime import timedelta
from unittest.mock import MagicMock
from classes import *
from services import BusinessRules


class TestBusinessRules(unittest.TestCase):
    def setUp(self):
        self.client_repository = MagicMock()
        self.courier_repository = MagicMock()
        self.order_repository = MagicMock()
        self.comment_repository = MagicMock()

        self.service = BusinessRules(
            client_repository=self.client_repository,
            courier_repository=self.courier_repository,
            orders_repository=self.order_repository,
            comments_repository=self.comment_repository
        )

    def test_make_order(self):  # add_order вызван
        user_id = 1
        delivery_address = "test address"
        items = [Burger(1, "borgar"), BurgerSet(1, "borgars", [Burger(1, "borgar"), Burger(1, "borgar")])]

        self.service.make_order(user_id, delivery_address, items)
        self.order_repository.add_order.assert_called_once()

    def test_mark_order_as_taken(self):  # соответствует ли id курьера ожидаемому
        order_id = 1
        courier_id = 2
        client = Client(1, "client", "312")
        courier = Courier(courier_id, "courier")
        items = [Burger(1, "borgar"), BurgerSet(1, "borgars", [Burger(1, "borgar"), Burger(1, "borgar")])]
        test_order = Order(order_id, client, datetime.now(), None,
                           "address", None, items,
                           sum(300 if isinstance(item, Burger) else 800 for item in items))

        self.order_repository.find_by_id.return_value = test_order
        self.courier_repository.find_by_id.return_value = courier

        self.service.mark_order_as_taken(order_id, courier_id)
        self.assertEqual(test_order.courier.id, courier_id)

    def test_mark_order_as_delivered(self):  # дата установлена
        client = Client(1, "client", "3123")
        courier = Courier(1, "courier")
        items = [Burger(1, "borgar"), BurgerSet(1, "borgars", [Burger(1, "borgar"), Burger(1, "borgar")])]
        test_order = Order(1, client, datetime.now(), None,
                           "address", courier, items,
                           sum(300 if isinstance(item, Burger) else 800 for item in items))

        self.order_repository.find_by_id.return_value = test_order
        self.courier_repository.find_by_id.return_value = courier

        self.service.mark_order_as_delivered(1, 1)
        self.assertIsNotNone(test_order.delivery_time)

    def test_leave_comment(self):  # add_comment вызван
        order_id = 1
        user_id = 2
        comment_text = "comment"

        self.service.leave_comment(order_id, user_id, comment_text)
        self.comment_repository.add_comment.assert_called_once()

    def test_check_delivery_time(self):  # цена уменьшилась
        order_id = 1
        client = Client(1, "client", "3123")
        courier = Courier(1, "courier")
        items = [Burger(1, "borgar"), BurgerSet(1, "borgars", [Burger(1, "borgar"), Burger(1, "borgar")])]

        creation_time = datetime.now() - timedelta(hours=3)
        delivery_time = datetime.now()

        test_order = Order(1, client, creation_time, delivery_time,
                           "address", courier, items,
                           sum(300 if isinstance(item, Burger) else 800 for item in items))

        self.order_repository.find_by_id.return_value = test_order
        self.courier_repository.find_by_id.return_value = courier

        self.service.check_delivery_time(order_id)
        self.assertEqual(test_order.price, sum(300 if isinstance(item, Burger) else 800 for item in items) // 2)
