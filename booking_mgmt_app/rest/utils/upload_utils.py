import csv

from bson import ObjectId
from flask_restplus import marshal

from rest import entity_mgmt_app as application
from rest.utils.db_service import Base
from rest.common.constants import BOOKING_COLLECTION, ENTITY_TYPE_COLLECTION, \
    ENTITY_TEMPLATE_COLLECTION
from rest.common.enums import ENTITY_TYPES
from rest.entities.templates.models import entity_template
from rest.entity_types.models import entity_type

ENTITY_TEMPLATES_PATH = application.config.get('TEMPLATES_PATH') + "/entity_templates"
ENTITY_PATH = application.config.get('TEMPLATES_PATH') + "/entities"

db_client = Base()


def custom_marshal(req_data, resp_data):
    """
    customize marshal
    :param req_data:
    :param resp_data:
    :return:
    """
    data = marshal(req_data, resp_data)
    if data.get('type') != ENTITY_TYPES.ORGANIZATION.value:
        data['parent'] = ObjectId(data.get('parent'))
    return data


def get_entities_with_values(file_name, entity_template):
    """
    generate entities with values
    :param file_name:
    :param entity_template:
    :return:
    """
    entity_with_values_list = []
    with open(file_name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        field_names = []
        for row in csv_reader:
            field_name_values = {}
            if line_count == 0:
                field_names = row
            else:
                # entity_template_dup = entity_template.copy()
                for item in field_names:
                    field_name_values[item] = ''
                i = 0
                for value in row:
                    field_name_values[field_names[i]] = value
                    i += 1
                entity_with_values_list.append(field_name_values)

            line_count += 1
        return entity_with_values_list


def get_entity_templates_with_values(file_name):
    """
    generate  entity templates with values
    :param file_name:
    :return:
    """
    entity_templates_with_values_list = []
    with open(file_name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        field_names = []
        for row in csv_reader:
            field_name_values = {}
            if line_count == 0:
                field_names = row
            else:
                # entity_template_dup = entity_template.copy()
                for item in field_names:
                    field_name_values[item] = ''
                i = 0
                for value in row:
                    field_name_values[field_names[i]] = value
                    i += 1
                entity_templates_with_values_list.append(field_name_values)

            line_count += 1
        return entity_templates_with_values_list


def insert_entity(entity):
    """
    Insert entity Or Check whether it is already present.
    :param entity:
    :return: Id
    """
    _count, _records = db_client.get(BOOKING_COLLECTION, {"name": entity.get('name')})
    if _count >= 1 and _records:
        entity_id = _records[0].get('_id')
        print(f"Asset {_records[0].get('name')} already present")
    else:
        entity_res, entity_id = db_client.create(BOOKING_COLLECTION, custom_marshal(entity, entity))
        print(f"Asset Id: {entity_id} & Name: {entity.get('name')} inserted successfully.")
    return entity_id


def insert_entity_type(entity):
    """
    Insert entity Or Check whether it is already present.
    :param entity:
    :return: Id
    """
    _count, _records = db_client.get(ENTITY_TYPE_COLLECTION, {"name": entity.get('name')})
    if _count >= 1 and _records:
        entity = _records[0]
        entity_id = _records[0].get('_id')
        print(f"Entity Type {_records[0].get('name')} already present")
    else:
        entity_res, entity_id = db_client.create(ENTITY_TYPE_COLLECTION, custom_marshal(entity, entity_type))
        _count, _records = db_client.get(ENTITY_TYPE_COLLECTION, {"name": entity.get('name')})
        entity = _records[0]
        print(f"Entity Type Id: {entity_id} & Name: {entity.get('name')} inserted successfully.")
    return entity_id, entity
