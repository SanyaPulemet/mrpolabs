from classes import *


class ClientRepository:

    def __init__(self):
        self.clients = []

    def add_client(self, client: Client):
        self.clients.append(client)

    def delete_client(self, client: Client):
        self.clients.remove(client)

    def find_by_id(self, id):
        for c in self.clients:
            if c.id == id:
                return c

    def get_all_clients(self):
        for c in self.clients:
            print(f"{c.name}; {c.phone};")


class CommentsRepository:

    def __init__(self):
        self.comments = []

    def add_comment(self, comment: Comment):
        self.comments.append(comment)

    def delete_comment(self, comment: Comment):
        self.comments.remove(comment)

    def find_by_id(self, id):
        for c in self.comments:
            if c.id == id:
                return c

    def get_all_comments(self):
        for c in self.comments:
            print(f"{c.text}; {c.client.name}; {c.order.id};")


class OrdersRepository:

    def __init__(self):
        self.orders = []

    def add_order(self, order: Order):
        self.orders.append(order)

    def delete_order(self, order: Order):
        self.orders.remove(order)

    def find_by_id(self, id):
        for s in self.orders:
            if s.id == id:
                return s

    def get_all_orders(self):
        for o in self.orders:
            print(f"{o.id}; {o.client.name}; {o.courier.name}; {o.items};")