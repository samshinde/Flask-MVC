from bson import ObjectId
from flask_restplus import fields

from rest import api
from rest.common.base_models import meta, tag
# from rest.booking.models import entity_type_response
from rest.utils.dateutils import reformat
from datetime import datetime


class Fields(fields.Raw):
    def format(self, data):
        for key, value in data.items():
            if isinstance(value, datetime):
                data[key] = reformat(value, '%m/%d/%Y %H:%M')
        return data


booking_request = api.model('booking request', {
    'entity_name': fields.String(required=True, description='entity name'),
    'entity_id': fields.String(required=True, description='entity id'),
    'quantity': fields.String(required=True, description='quantity'),
    'fields': Fields(description='fields', default={})
})

booking_update_request = api.inherit('booking update', booking_request, {

})

booking_entity = api.inherit('bookings', booking_request, {
    'meta': fields.Nested(meta),
    'tags': fields.List(fields.Nested(tag)),
    'booking_status': fields.String(default='', description='booking status'),
})

booking_response = api.inherit('booking response', booking_entity, {
    '_id': fields.String(),
})

booking_delete_request = api.model('booking_delete_request', {
    "booking_ids": fields.List(fields.String())
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
