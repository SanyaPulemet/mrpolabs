import inspect
import uuid
from classes import *
import xml.dom.minidom
import xml.etree.ElementTree as ET
from datetime import datetime
from uuid import uuid4, UUID
from dateutil import parser
import json
from sqlarepo import AbstractRepository


class JsonRepo(AbstractRepository):

    def __init__(self, data):
        self.data = create_entities_dict_from_json('output.json', class_registry, conversion_registry)

    def create(self, entity):
        self.data[entity.id] = entity
        serialize_list_to_json(list(self.data.values()))
        self.data = create_entities_dict_from_json('output.json', class_registry, conversion_registry)
        return entity

    def get(self, id):
        return self.data[id]

    def list(self):
        return list(self.data.values())

    def update(self, entity):
        obj = self.get(entity.id)
        if obj:
            self.data[obj.id] = entity
            serialize_list_to_json(list(self.data.values()))
            self.data = create_entities_dict_from_json('output.json', class_registry, conversion_registry)
            return obj
        return None

    def delete(self, entity):
        if self.get(entity.id):
            self.data.pop(entity.id)
            serialize_list_to_json(list(self.data.values()))
            self.data = create_entities_dict_from_json('output.json', class_registry, conversion_registry)
            return True
        return False


def serialize_to_json(entity):
    entity_dict = {}

    for attr_name, attr_value in entity.__dict__.items():
        if isinstance(attr_value, (Burger, BurgerSet, Courier, Client, Order, Comment)):
            entity_dict[attr_name] = str(attr_value.id)
        elif isinstance(attr_value, (str, int, float, UUID, datetime)) or attr_value is None:
            entity_dict[attr_name] = str(attr_value)
        elif isinstance(attr_value, list):
            serialized_list = []
            for item in attr_value:
                if hasattr(item, 'id'):
                    serialized_list.append(str(item.id))
                else:
                    serialized_list.append(serialize_to_json(item))
            entity_dict[attr_name] = serialized_list
        else:
            entity_dict[attr_name] = str(attr_value)

    return json.dumps(entity_dict)


def serialize_list_to_json(entities):
    entities_list = [json.loads(serialize_to_json(entity)) for entity in entities]
    return json.dumps(entities_list)

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


def create_entity_from_json(type_name, json_data, class_registry, conversion_registry):
    entity_data = {}

    entity_class = class_registry.get(json_data.get('type'))
    if not entity_class:
        raise ValueError(f"No class registered for type: {json_data.get('type')}")

    for key, value in json_data.items():
        if key in conversion_registry:
            # Функция преобразования для уникальных (должных к обработке) полей
            print(key, ' ', value)
            converted_value = conversion_registry[key](value)
            entity_data[key] = converted_value
        else:
            entity_data[key] = value

    # Приведение параметров к иниту класса
    constructor_params = inspect.signature(entity_class).parameters
    init_args = {param: entity_data[param] for param in constructor_params if param in entity_data}

    return entity_class(**init_args)

def create_entities_dict_from_json(file_path, class_registry, conversion_registry):
    entities = {}
    with open(file_path, 'r') as file:
        data = json.load(file)

    for type_name, items in data.items():
        if not isinstance(items, list):  # Если не список, оборачивание в список
            items = [items]
        for item in items:
            item['type'] = type_name  # Добавляем тип в каждый элемент для create_entity
            entity = create_entity_from_json(type_name, item, class_registry, conversion_registry)
            entities[entity.id] = entity

    for entity_id, entity in entities.items():
        for attr_name in dir(entity):
            if not attr_name.startswith("__") and attr_name != 'id':
                attr_value = getattr(entity, attr_name)

                if isinstance(attr_value, uuid.UUID):  # Замена одиночного UUID
                    if entities.get(attr_value) is not None and entities.get(attr_value) != "None":
                        setattr(entity, attr_name, entities.get(attr_value))

                elif isinstance(attr_value, list) and all(isinstance(item, uuid.UUID) for item in attr_value):
                    # Замена списка UUIDs
                    updated_list = [entities.get(item) for item in attr_value]
                    setattr(entity, attr_name, updated_list)

    return entities

entities = create_entities_dict_from_json('output.json', class_registry, conversion_registry)

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
