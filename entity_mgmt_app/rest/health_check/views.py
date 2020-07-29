#!/usr/bin/env python
from flask import request
from flask_restplus import Resource, Namespace

from rest import api, auth_header_parser
from rest.health_check.models import application_status
from rest.health_check.service import ApplicationStatusService
from rest.common.constants import SUCCESS

# TODO:  from rest.auth.utils import admin_required

health_check_api_ns = Namespace('health_check', description='auth operation')

APPLICATION_STATUS_SERVICE = ApplicationStatusService()


@api.expect(auth_header_parser)
@health_check_api_ns.route('/')
class Status(Resource):
    """
    Status or Health Check
    """

    def get(self):
        """
        status of the application
        :return: returns status
        """
        return APPLICATION_STATUS_SERVICE.get_application_status()

    # TODO: @admin_required
    @api.expect(application_status, validate=True)
    def post(self):
        """
        set status of application
        :return:
        """
        APPLICATION_STATUS_SERVICE.update_application_status(request.get_json())
        return {"status": SUCCESS, "message": "application status updated successfully"}
