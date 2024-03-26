from __future__ import annotations
from typing import List, Union, Optional
from datetime import datetime
from dataclasses import dataclass


@dataclass(frozen=True)
class Burger:
    id: int
    name: str


@dataclass(frozen=True)
class BurgerSet:
    id: int
    name: str
    burgers: List[Burger]


class Courier:
    def __init__(self, id, name, orders: List[Order]):
        self.id = id
        self.name = name
        self.orders = orders

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return self.id == other.id and self.name == other.name
        return False


class Client:
    def __init__(self, id, name, phone, orders: List[Order], comments: List[Comment]):
        self.id = id
        self.name = name
        self.phone = phone
        self.orders = orders
        self.comments = comments

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return self.id == other.id and self.name == other.name
        return False


class Order:
    def __init__(self, id, client: Client, creation_time, delivery_time: datetime | None,
                 delivery_address, courier: Courier | None, items: List[Union[Burger, BurgerSet]], price):
        self.id = id
        self.client = client
        self.creation_time = creation_time
        self.delivery_time = delivery_time
        self.delivery_address = delivery_address
        self.courier = courier
        self.items = items
        self.price = price

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return self.id == other.id and self.client == other.client
        return False


@dataclass(frozen=True)
class Comment:
    id: int
    text: str
    client: Client
    order: Order
