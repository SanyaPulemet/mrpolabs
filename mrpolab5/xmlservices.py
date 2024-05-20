from datetime import datetime, timedelta

import services
from classes import *
from sqla import *
import sqla
from services import *
from xmllayer import *
from uuid import uuid4, UUID


class BusinessRules:
    rules = services.BusinessRules()
    dict = create_entities_dict_from_xml()
    def make_order(self, user: UUID, delivery_address, items):
        return self.rules.make_order(self.dict.get(user), delivery_address, items)

    def mark_order_as_taken(self, order: UUID, courier: UUID):
        print(self.dict.get(order))
        return self.rules.mark_order_as_taken(self.dict.get(order),
                                              self.dict.get(courier))

    def mark_order_as_delivered(self, order: UUID, courier: UUID):
        dict = create_entities_dict_from_xml()
        return self.rules.mark_order_as_delivered(dict.get(order), dict.get(courier))

    def leave_comment(self, order: UUID,  user: UUID, comment_text):
        dict = create_entities_dict_from_xml()
        return self.rules.leave_comment(dict.get(order), dict.get(user), comment_text)

    def check_delivery_time(self, order: UUID):
        dict = create_entities_dict_from_xml()
        return self.rules.check_delivery_time(dict.get(order))


xmlrules = BusinessRules()

dict = create_entities_dict_from_xml()

print(xmlrules.make_order(uuid.UUID('0b20ddc1-0f2f-404a-9eda-4eb3fe2775bb'),
                          'das',[]))
print()
print(xmlrules.mark_order_as_taken(uuid.UUID('641d6cd8-64ee-4d01-832d-bd364d6502ca'),
                                   uuid.UUID('d11df454-2d0a-46d4-8941-27dd6b66a156')))
print()
print(xmlrules.mark_order_as_delivered(uuid.UUID('641d6cd8-64ee-4d01-832d-bd364d6502ca'),
                                       uuid.UUID('d11df454-2d0a-46d4-8941-27dd6b66a156')))
print()
print(xmlrules.leave_comment(uuid.UUID('641d6cd8-64ee-4d01-832d-bd364d6502ca'),
                             uuid.UUID('0b20ddc1-0f2f-404a-9eda-4eb3fe2775bb'),
                             'txt'))
print()
print(xmlrules.check_delivery_time(uuid.UUID('641d6cd8-64ee-4d01-832d-bd364d6502ca')))
print()