import inspect
import uuid
from classes import *
import xml.dom.minidom
import xml.etree.ElementTree as ET
from datetime import datetime
from uuid import uuid4, UUID
from dateutil import parser
#from dataclasses import is_dataclass, replace, fields

# junk code
'''# region Write funcs
# Функция для сериализации Burger в XML Element
def serialize_burger(burger):
    burger_element = ET.Element('Burger')
    burger_element.set('id', str(burger.id))
    burger_element.set('name', burger.name)
    return burger_element

# Аналогичные функции для других классов...
from xml.etree.ElementTree import SubElement


def serialize_burgerset(burgerset):
    burgerset_element = ET.Element('BurgerSet')
    burgerset_element.set('id', str(burgerset.id))
    burgerset_element.set('name', burgerset.name)
    for burger in burgerset.burgers:
        burger_ref = SubElement(burgerset_element, 'Burger')
        burger_ref.set('ref', str(burger.id))
    return burgerset_element


def serialize_courier(courier):
    courier_element = ET.Element('Courier')
    courier_element.set('id', str(courier.id))
    courier_element.set('name', courier.name)
    for order in courier.orders:
        order_ref = SubElement(courier_element, 'Order')
        order_ref.set('ref', str(order.id))
    return courier_element


def serialize_client(client):
    client_element = ET.Element('Client')
    client_element.set('id', str(client.id))
    client_element.set('name', client.name)
    client_element.set('phone', client.phone)
    for order in client.orders:
        order_ref = SubElement(client_element, 'Order')
        order_ref.set('ref', str(order.id))
    for comment in client.comments:
        comment_ref = SubElement(client_element, 'Comment')
        comment_ref.set('ref', str(comment.id))
    return client_element


def serialize_order(order):
    order_element = ET.Element('Order')
    order_element.set('id', str(order.id))

    if order.client is not None:
        client_ref = SubElement(order_element, 'Client')
        client_ref.set('ref', str(order.client.id))

    order_creation_time = SubElement(order_element, 'CreationTime')
    order_creation_time.text = order.creation_time.isoformat()

    if order.delivery_time is not None:
        delivery_time = SubElement(order_element, 'DeliveryTime')
        delivery_time.text = order.delivery_time.isoformat()

    delivery_address = SubElement(order_element, 'DeliveryAddress')
    delivery_address.text = order.delivery_address

    if order.courier is not None:
        courier_ref = SubElement(order_element, 'Courier')
        courier_ref.set('ref', str(order.courier.id))

    items = SubElement(order_element, 'Items')

    for item in order.items:
        if isinstance(item, Burger):
            burger_ref = SubElement(items, 'Burger')
            burger_ref.set('ref', str(item.id))
        elif isinstance(item, BurgerSet):
            burgerset_ref = SubElement(items, 'BurgerSet')
            burgerset_ref.set('ref', str(item.id))

    price = SubElement(order_element, 'Price')
    price.text = str(order.price)

    return order_element


def serialize_comment(comment):
    comment_element = ET.Element('Comment')

    comment_text = SubElement(comment_element, 'Text')
    comment_text.text = comment.text

    if comment.client is not None:
        client_ref = SubElement(comment_element, 'Client')
        client_ref.set('ref', str(comment.client.id))

    if comment.order is not None:
        order_ref = SubElement(comment_element, 'Order')
        order_ref.set('ref', str(comment.order.id))

    comment_id = ET.SubElement(comment_element, "ID")
    comment_id.text = str(comment.id)

    return comment_id


# Создание корневого элемента и добавление объектов в него (пример)

# Функция для сохранения корневого элемента в файл XML
def prettify(elem):
    """Возвращает красиво отформатированную строку XML для элемента."""
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

def save_to_xml(root_element, file_name):
    """Сохраняет корневой элемент в файл XML с красивым форматированием."""
    pretty_xml_as_string = prettify(root_element)
    with open(file_name, 'w') as f:
        f.write(pretty_xml_as_string)
# endregion

# region write tests
# Создание корневого элемента
root = ET.Element('Root')

# Добавление объектов в корневой элемент (пример)
# Создание примеров объектов
burger1 = Burger(name="Classic Burger")
burger2 = Burger(name="Veggie Burger")

burgerset1 = BurgerSet(name="Family Pack", burgers=[burger1, burger2])

client1 = Client(name="Alice", phone="1234567890", orders=[], comments=[])
client2 = Client(name="Bob", phone="0987654321", orders=[], comments=[])

comment1 = Comment(text="Loved the burgers!", client=client1, order=None)
comment2 = Comment(text="Great service.", client=client2, order=None)

order1 = Order(
    client=client1,
    creation_time=datetime.now(),
    delivery_time=None,
    delivery_address="123 Main Street",
    courier=None,
    items=[burgerset1],
    price=29.99
)

courier1 = Courier(name="Dave", orders=[order1])

# Обновляем списки заказов и комментариев клиентов после создания заказов и комментариев
client1.orders.append(order1)
client1.comments.append(comment1)

client2.comments.append(comment2)

# Создание корневого элемента XML и добавление всех объектов
root = ET.Element('Root')
root.append(serialize_burger(burger1))
root.append(serialize_burger(burger2))
root.append(serialize_burgerset(burgerset1))
root.append(serialize_client(client1))
root.append(serialize_client(client2))
root.append(serialize_comment(comment1))
root.append(serialize_comment(comment2))
root.append(serialize_order(order1))
root.append(serialize_courier(courier1))

# Сохранение корневого элемента в файл XML
save_to_xml(root, 'data.xml')
# endregion

# region read and create

# endregion

# region read and create tests

# endregion'''

'''def serialize_to_xml(entity):
    xml_elements = []

    # Открывающий тег с именем класса объекта - корневой элемент
    xml_elements.append(f"<{entity.__class__.__name__}>")

    for attr_name, attr_value in entity.__dict__.items():
        if isinstance(attr_value, str) or isinstance(attr_value, int) or isinstance(attr_value, datetime) or attr_value == None:
            # Прямая сериализация строковых и числовых значений
            xml_elements.append(f"<{attr_name}>{attr_value}</{attr_name}>")
        elif hasattr(attr_value, 'id'):
            # Сериализация ссылочного объекта по ID
            xml_elements.append(f"<{attr_name}>{attr_value.id}</{attr_name}>")
        elif isinstance(attr_value, list):
            # Для списков необходимо обработать каждый элемент отдельно
            xml_elements.append(f"<{attr_name}>")
            for item in attr_value:
                if hasattr(item, 'id'):
                    xml_elements.append(str(item.id))
                    xml_elements.append(str(','))
                else:
                    # Рекурсивная сериализация для вложенных сущностей без ID
                    xml_elements.extend(serialize_to_xml(item))
            xml_elements.append(f"</{attr_name}>")
        else:
            # Рекурсивная сериализация для вложенных сущностей
            xml_elements.extend(serialize_to_xml(attr_value))

    # Закрывающий тег с именем класса объекта - корневой элемент
    xml_elements.append(f"</{entity.__class__.__name__}>")

    return "".join(xml_elements)'''


def serialize_to_xml(entity):
    xml_elements = []
    xml_elements.append(f"<{entity.__class__.__name__}>")

    for attr_name, attr_value in entity.__dict__.items():
        if isinstance(attr_value, (Burger, BurgerSet, Courier, Client, Order, Comment)):
            xml_elements.append(f"<{attr_name}>{str(attr_value.id)}</{attr_name}>")
        elif isinstance(attr_value, (str, int, float, UUID, datetime)) or attr_value is None:
            value = str(attr_value)
            xml_elements.append(f"<{attr_name}>{value}</{attr_name}>")
        elif isinstance(attr_value, list):
            xml_elements.append(f"<{attr_name}>")
            for item in attr_value:
                if hasattr(item, 'id'):
                    xml_elements.append(str(item.id))
                    xml_elements.append(str(','))
                else:
                    xml_elements.extend(serialize_to_xml(item))
            xml_elements.append(f"</{attr_name}>")
        else:
            xml_elements.append(f"<{attr_name}>{value}</{attr_name}>")

    xml_elements.append(f"</{entity.__class__.__name__}>")
    return "".join(xml_elements)


def serialize_list_to_xml(entities):
    xml_elements = ["<Entities>"]

    for entity in entities:
        xml_elements.append(serialize_to_xml(entity))

    xml_elements.append("</Entities>")

    return "".join(xml_elements)


def pretty_print_xml(unformatted_xml: str) -> str:
    dom = xml.dom.minidom.parseString(unformatted_xml.encode('utf-8'))
    return dom.toprettyxml(indent="  ")


class_registry = {
    'Order': Order,
    'Courier': Courier,
    'Burger': Burger,
    'BurgerSet': BurgerSet,
    'Client': Client,
    'Comment': Comment,
}


def convert_to_date(date_string):
    try:
        return parser.parse(date_string)
    except ValueError as e:
        return None


def convert_string_to_float(string):
    if string is None or string == "None":
        return None
    return float(string)


def convert_string_to_uuid(string):
    if string and string != "None":
        return uuid.UUID(string)
    return None


def split_string_to_uuid_list(string):
    if string is None or string == "None":
        return None
    return [uuid.UUID(s.strip()) for s in string.split(',') if s.strip()]


conversion_registry = {
    'id': convert_string_to_uuid,
    'creation_time': convert_to_date,
    'delivery_time': convert_to_date,
    'price': convert_string_to_float,
    'burgers': split_string_to_uuid_list,
    'orders': split_string_to_uuid_list,
    'comments': split_string_to_uuid_list,
    'items': split_string_to_uuid_list,
    'courier': convert_string_to_uuid,
    'client': convert_string_to_uuid,
}


def create_entity_from_xml(xml_element, class_registry, conversion_registry):
    entity_data = {}
    for child in xml_element:
        if child.tag in conversion_registry:
            # функция преобразования для уникальных(должных к обработке) полей
            converted_value = conversion_registry[child.tag](child.text)
            entity_data[child.tag] = converted_value
        else:
            entity_data[child.tag] = child.text

    entity_class = class_registry.get(xml_element.tag)
    if not entity_class:
        raise ValueError(f"No class registered for tag: {xml_element.tag}")

    # приведение параметров к иниту класса
    constructor_params = inspect.signature(entity_class).parameters
    init_args = {param: entity_data[param] for param in constructor_params if param in entity_data}
    #print(init_args)

    return entity_class(**init_args)

def create_entities_dict_from_xml():
    entities = {}

    with open('output.xml', 'r') as file:
        root = ET.parse(file).getroot()

    for child in root:
        entity = create_entity_from_xml(child, class_registry, conversion_registry)
        entities[entity.id] = entity

    for entity_id, entity in entities.items():
        for attr_name in dir(entity):
            if not attr_name.startswith("__") and attr_name != 'id':
                attr_value = getattr(entity, attr_name)
                #print(attr_name, attr_value, type(attr_value))

                if isinstance(attr_value, uuid.UUID):  # замена одиночного UUID
                    #print(attr_name, attr_value, type(attr_value))
                    if entities.get(attr_value) is not None and entities.get(attr_value) != "None":
                        #print(attr_name, attr_value, type(attr_value))
                        setattr(entity, attr_name, entities.get(attr_value))
                elif isinstance(attr_value, list) and all(isinstance(item, uuid.UUID) for item in attr_value):
                    # замена списка UUIDs
                    #print(attr_name, attr_value, type(attr_value))
                    updated_list = [entities.get(item) for item in attr_value]
                    setattr(entity, attr_name, updated_list)

    return entities

entities = create_entities_dict_from_xml()


def print_entities_with_uuid(entity_dict):
    for entity_uuid, entity in entity_dict.items():
        entity_name = entity.__class__.__name__

        # Получаем все поля сущности
        fields = vars(entity)
        print(f"UUID: {entity_uuid}, Entity Name: {entity_name}")
        for field_name, field_value in fields.items():
            field_type = type(field_value).__name__
            print(f"  Field Name: {field_name}, Field Value: {field_value}, Field Type: {field_type}")


print_entities_with_uuid(entities)


'''entities = [create_entity_from_xml(child, class_registry, conversion_registry) for child in root]

for entity in entities:
    print(f"Entity: {entity.__class__.__name__}")
    for field_name, field_value in vars(entity).items():
        # Получение типа поля с помощью функции type()
        field_type = type(field_value).__name__
        print(f"Field Name: {field_name}, Field Value: {field_value}, Field Type: {field_type}")'''

# write tests
'''# region write tests
# root = ET.Element('Root')

burger1 = Burger(name="Classic Burger")
burger2 = Burger(name="Veggie Burger")

burgerset1 = BurgerSet(name="Family Pack", burgers=[burger1, burger2])

client1 = Client(name="Alice", phone="1234567890", orders=[], comments=[])
client2 = Client(name="Bob", phone="0987654321", orders=[], comments=[])

comment1 = Comment(text="Loved the burgers!", client=client1, order=None)
comment2 = Comment(text="Great service.", client=client2, order=None)

order1 = Order(
    client=client1,
    creation_time=datetime.now(),
    delivery_time=None,
    delivery_address="123 Main Street",
    courier=None,
    items=[burgerset1, burgerset1],
    price=29.99
)

courier1 = Courier(name="Dave", orders=[order1])

client1.orders.append(order1)
client1.comments.append(comment1)

client2.comments.append(comment2)

xml_output = serialize_list_to_xml([order1, courier1])
pretty_xml = pretty_print_xml(xml_output)

with open('output.xml', 'w') as file:
    file.write(pretty_xml)
# endregion'''


