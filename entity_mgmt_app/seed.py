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
    locality = {"name": "bhosari", "type": ENTITY_TYPES.LOCALITY.value, "display_name": "Bhosari"}
    locality_id, locality_resp = insert_entity_type(locality)
    locality = {"name": "moshi", "type": ENTITY_TYPES.LOCALITY.value, "display_name": "Moshi"}
    locality_id, locality_resp = insert_entity_type(locality)
    locality = {"name": "charholi", "type": ENTITY_TYPES.LOCALITY.value, "display_name": "Charholi"}
    locality_id, locality_resp = insert_entity_type(locality)

    organization = {"name": "org", "type": ENTITY_TYPES.ORGANIZATION.value, "display_name": "Quantum"}
    org_id, org_resp = insert_entity_type(organization)

    workspace = {"name": "workspace", "type": ENTITY_TYPES.WORKSPACE.value, "display_name": "My Workspace",
                 "parent": org_id}
    workspace_id, workspace_resp = insert_entity_type(workspace)

    # Entity type Vegetable
    vegetables = {"name": "vegetables", "type": ENTITY_TYPES.ITEM.value, "display_name": "Vegetables",
                  "parent": workspace_id}
    vegetables_id, vegetables_resp = insert_entity_type(vegetables)

    # Vegetable templates
    veg_templates_with_values = get_entity_templates_with_values(ENTITY_TEMPLATES_PATH + "/vegetable_template.csv")

    veg_template = dict()
    veg_template["entity_type"] = ENTITY_TYPES.ITEM.value
    veg_template["entity_type_details"] = vegetables_resp
    veg_template["fields"] = []

    for v in veg_templates_with_values:
        veg_template["fields"].append(v)
    veg_template_id, veg_template_res = insert_entity_template(veg_template)

    # Vegetables
    veg_with_values = get_entities_with_values(ENTITY_PATH + "/vegetables.csv", veg_template_res)

    veg_entity = dict()
    veg_entity["entity_type"] = ENTITY_TYPES.ITEM.value
    veg_entity["entity_type_details"] = vegetables_resp
    veg_entity["fields"] = []

    for v in veg_with_values:
        veg_entity["fields"].append(v)

    veg_entity_id, veg_entity_res = insert_entity(veg_entity)

    # Entity type Marriage hall : id, name, description, icon
    marriage_hall = {"name": "marriage_hall", "type": ENTITY_TYPES.ITEM.value, "display_name": "Marriage Hall",
                     "parent": workspace_id}
    marriage_hall_id, marriage_hall_resp = insert_entity_type(vegetables)

    # Marriage hall templates
    mar_hall_templates_with_values = get_entity_templates_with_values(
        ENTITY_TEMPLATES_PATH + "/marriage_hall_template.csv")

    mar_hall_template = dict()
    mar_hall_template["entity_type"] = ENTITY_TYPES.ITEM.value
    mar_hall_template["entity_type_details"] = marriage_hall_resp
    mar_hall_template["fields"] = []

    for v in mar_hall_templates_with_values:
        mar_hall_template["fields"].append(v)
    mar_hall_template_id, mar_hall_template_res = insert_entity_template(mar_hall_template)

    # Marriage hall
    mar_hall_with_values = get_entities_with_values(ENTITY_PATH + "/marriage_halls.csv", mar_hall_template_res)

    mar_hall_entity = dict()
    mar_hall_entity["entity_type"] = ENTITY_TYPES.ITEM.value
    mar_hall_entity["entity_type_details"] = marriage_hall_resp
    mar_hall_entity["fields"] = []

    for v in mar_hall_with_values:
        mar_hall_entity["fields"].append(v)

    mar_hall_entity_id, mar_hall_entity_res = insert_entity(mar_hall_entity)


if __name__ == '__main__':
    print("Initialize seed data")
    seed()
    print("Inserted seed data.")
    exit(1)
