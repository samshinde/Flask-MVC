import datetime
from flask_restplus import fields
from rest import api


class DateTimeISO(fields.String):
    """
    Custom Format to modify time to ISO Format
    """

    def format(self, value):
        modified_date = value + 'Z'
        return modified_date


meta = api.model('meta', {
    'is_deleted': fields.Boolean(default=False),
    'created': DateTimeISO(),
    'updated': DateTimeISO(),
    'created_by': fields.String(default=''),
    'updated_by': fields.String(default=''),
})

audit = api.model('audit event', {
    'meta': fields.Nested(meta),
    'method': fields.String(description='method'),
    'endpoint': fields.String(description='endpoint'),
    'message': fields.String(description='message'),
    'result': fields.Raw(description='fields', default={}),
    'status': fields.Integer(description='status'),
    'event': fields.String(description='event'),
    'req_data': fields.Raw(default={}, description='req_data'),
    'query_param': fields.Raw(description='query_param')
})

audit_response = api.inherit('audit response', audit, {
    '_id': fields.String()
})
