from typing import List, Union


class Courier:
    def __init__(self, id, name):
        self.id = id
        self.name = name


class Client:
    def __init__(self, id, name, phone):
        self.id = id
        self.name = name
        self.phone = phone


class Burger:
    def __init__(self, id, name):
        self.id = id
        self.name = name


class BurgerSet:
    def __init__(self, id, name, burgers: List[Burger]):
        self.id = id
        self.name = name
        self.burgers = burgers


class Order:
    def __init__(self, id, client: Client, delivery_time,
                 delivery_address, courier: Courier, items: List[Union[Burger, BurgerSet]], price):
        self.id = id
        self.client = client
        self.delivery_time = delivery_time
        self.delivery_address = delivery_address
        self.courier = courier
        self.items = items
        self.price = price


class Comment:
    def __init__(self, id, text, client: Client, order: Order):
        self.id = id
        self.text = text
        self.client = client
        self.order = order
