#!/usr/bin/env python

from rest import entity_mgmt_app as application
from rest.common.enums import ENTITY_TYPES
from rest.utils.db_service import Base
from rest.utils.upload_utils import insert_entity, insert_entity_template, insert_entity_type, \
    get_entity_templates_with_values, get_entities_with_values

ENTITY_TEMPLATES_PATH = application.config.get('TEMPLATES_PATH') + "/entity_templates"
ENTITY_PATH = application.config.get('TEMPLATES_PATH') + "/entities"

db_client = Base()


def seed():
    """
    seed data into database
    :return:
    """
    booking1 = {"entity_id": "", "entity_type": ENTITY_TYPES.ITEM.value, "quantity": "1"}
    locality_id, locality_resp = insert_entity_type(locality)


if __name__ == '__main__':
    print("Initialize seed data")
    seed()
    print("Inserted seed data.")
    exit(1)
