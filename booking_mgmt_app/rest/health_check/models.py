from flask_restplus import fields

from rest import api

application_status = api.model('application_status', {
    'status': fields.String(description='application status', required=True),
})
