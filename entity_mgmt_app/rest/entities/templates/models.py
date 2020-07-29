from flask_restplus import fields

from rest import api
from rest.common.base_models import meta, custom_fields
from rest.entity_types.models import entity_type_response

entity_template_request = api.model('entity_template_request', {
    'entity_type': fields.String(description='entity type', required=True),
    'force': fields.Boolean(description='force type', default=False, enum=[True, False]),
    'fields': fields.List(fields.Nested(custom_fields), description='custom_fields'),
})

entity_template = api.inherit('entity_template', entity_template_request, {
    'meta': fields.Nested(meta),
    'entity_type_details': fields.Nested(entity_type_response, description='entity type details'),
})

entity_template_response = api.inherit('entity_template_response', entity_template, {
    '_id': fields.String(description='unique id', required=True),
})
