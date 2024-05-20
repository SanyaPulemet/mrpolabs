from __future__ import annotations
from typing import List, Union, Optional
from datetime import datetime
from dataclasses import dataclass, field
from uuid import uuid4, UUID


@dataclass(frozen=True)
class Burger:
    name: str
    id: UUID = field(default_factory=uuid4)


@dataclass(frozen=True)
class BurgerSet:
    name: str
    burgers: List[Burger]
    id: UUID = field(default_factory=uuid4)


class Courier:
    def __init__(self, name, orders: List[Order], id: Optional[UUID] = None):
        self.id = id if id is not None else uuid4()
        self.name = name
        self.orders = orders

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return self.id == other.id and self.name == other.name
        return False


class Client:
    def __init__(self, name, phone, orders: List[Order], comments: List[Comment], id: Optional[UUID] = None):
        self.id = id if id is not None else uuid4()
        self.name = name
        self.phone = phone
        self.orders = orders
        self.comments = comments

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return self.id == other.id and self.name == other.name
        return False


class Order:
    def __init__(self, client: Client | None, creation_time, delivery_time: datetime | None,
                 delivery_address, courier: Courier | None, items: List[Union[Burger, BurgerSet]], price, id: Optional[UUID] = None):
        self.id = id if id is not None else uuid4()
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
    text: str
    client: Client | None
    order: Order | None
    id: UUID = field(default_factory=uuid4)
