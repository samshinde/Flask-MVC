from bson import ObjectId
from flask_restplus import fields

from rest import api
from rest.common.base_models import meta, tag
from rest.entity_types.models import entity_type_response
from rest.utils.dateutils import reformat
from datetime import datetime


class Fields(fields.Raw):
    def format(self, data):
        for key, value in data.items():
            if isinstance(value, datetime):
                data[key] = reformat(value, '%m/%d/%Y %H:%M')
        return data


entity_request = api.model('entity request', {
    'name': fields.String(required=True, description='entity name'),
    'parent': fields.String(description='parent entity'),
    'parent_type': fields.String(description='parent entity type'),
    'entity_type': fields.String(description='entity type', required=True),
    'fields': Fields(description='fields', default={})
})

entity_update_request = api.inherit('entity update', entity_request, {
    'parent_details': fields.Raw(description='fields', default={}),
})

entity = api.inherit('entities', entity_request, {
    'meta': fields.Nested(meta),
    'tags': fields.List(fields.Nested(tag)),
    'entity_type_details': fields.Nested(entity_type_response, description='entity type details'),
    'mgmt_status': fields.String(default='OK', description='mgmt status'),
    'parent_details': fields.Raw(description='fields', default={}),
})

entity_response = api.inherit('entitys_response', entity, {
    '_id': fields.String(),
})

entity_hierarchy_response = api.inherit('entity_hierarchy_response', entity_response, {
    'hierarchy': fields.List(fields.Nested(entity_response)),
})

entity_delete_request = api.model('entity_delete_request', {
    "entity_ids": fields.List(fields.String())
})


def set_bson_object(object, field, object_id):
    """
    set object id in for of mongo ObjectId
    :param object:
    :param field:
    :param object_id:
    :return:
    """
    if isinstance(object_id, str):
        object[field] = ObjectId(object_id)
    elif isinstance(object_id, ObjectId):
        object[field] = object_id
    return object
