from bson import ObjectId
from flask_restplus import fields

from rest import api
from rest.common.base_models import meta, tag
# from rest.entity_types.models import entity_type_response
from rest.utils.dateutils import reformat
from datetime import datetime


class Fields(fields.Raw):
    def format(self, data):
        for key, value in data.items():
            if isinstance(value, datetime):
                data[key] = reformat(value, '%m/%d/%Y %H:%M')
        return data


stock_request = api.model('stock request', {
    'entity_name': fields.String(required=True, description='entity name'),
    'entity_id': fields.String(required=True, description='entity id'),
    'availability': fields.Integer(required=True, description='availability'),
    'fields': Fields(description='fields', default={})
})

stock_update_request = api.inherit('stock update', stock_request, {

})

stock_entity = api.inherit('stock', stock_request, {
    'meta': fields.Nested(meta),
    'tags': fields.List(fields.Nested(tag)),
    'stock_status': fields.String(default='AVAILABLE', description='stock status'),
})

stock_response = api.inherit('stock response', stock_entity, {
    '_id': fields.String(),
})

stock_delete_request = api.model('stock_delete_request', {
    "stock_ids": fields.List(fields.String())
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
