import datetime
from flask_restplus import fields
from rest import api


meta = api.model('meta', {
    'is_deleted': fields.Boolean(default=False),
    'created': fields.DateTime(default=datetime.datetime.utcnow()),
    'updated': fields.DateTime(default=datetime.datetime.utcnow()),
    'created_by': fields.String(default=''),
    'updated_by': fields.String(default=''),
})

tag = api.model('tag', {
    'name': fields.String(description='Tag name', default=''),
    'value': fields.String(description='Tag value', default=''),
})

response = api.model('response', {
    'status': fields.Integer(description='Status code'),
    'message': fields.String(description='Message'),
    'data': fields.Raw(description='Response data', default={}),
})

custom_fields = api.model('field', {
    'name': fields.String(description='Field name', default=''),
    'value': fields.String(description='Field value', default=''),
    'type': fields.String(description='Field type', default=''),
    'is_required': fields.Boolean(description='Is required', default=False),
    'unique': fields.Boolean(description='Is unique', default=False),
    'options': fields.List(fields.String(), description='Options can be used', default=[]),
    'key': fields.String(description='Key', default=''),
    'is_header': fields.Boolean(description='is_header', default=False),
})
