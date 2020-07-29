from flask_restplus import fields

from rest import api
from rest.common.base_models import meta, custom_fields

entity_type_request = api.model('entity_type_request', {
    'name': fields.String(description='entity name', required=True),
    'display_name': fields.String(description='entity display name', required=True),
    'parent': fields.String(description='parent entity'),
    'type': fields.String(description='entity display name', enum=["ORGANIZATION", "WORKSPACE", "ITEM"], default=""),
    'fields': fields.List(fields.Nested(custom_fields), description='custom_fields')
})

entity_type = api.inherit('entity_type', entity_type_request, {
    'meta': fields.Nested(meta),
})

entity_type_response = api.inherit('entity_type_response', entity_type, {
    '_id': fields.String(description='unique id', required=True),
})
