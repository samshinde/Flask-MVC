from flask import request
from flask_jwt_extended import jwt_required
from flask_restplus import Resource, Namespace, reqparse

from rest import api, auth_header_parser
from rest.common.base_models import response
from rest.common.constants import SUCCESS
from rest.utils.dateutils import get_current_time, get_updated_time

from rest.audit.service import AuditEventService

audit_api_ns = Namespace('audit', description='audit operation')

AUDIT_SERVICE = AuditEventService()

pagination_parser = reqparse.RequestParser()
pagination_parser.add_argument('page', type=str, location='args')
pagination_parser.add_argument('size', type=str, location='args')
pagination_parser.add_argument('sort_by', type=str, location='args')
pagination_parser.add_argument('order_by', type=str, location='args')
pagination_parser.add_argument('start_date', type=str, location='args')
pagination_parser.add_argument('end_date', type=str, location='args')


@api.expect(auth_header_parser)
@audit_api_ns.route("/")
class AuditEventCollection(Resource):
    """
    Audit
    """

    @jwt_required
    @api.expect(pagination_parser)
    @api.marshal_with(response)
    def get(self):
        """
        list audit events
        :return: list of audit events
        """
        req_params = pagination_parser.parse_args(request)

        # remove None value from request
        req_params = {k: v for k, v in req_params.items() if v}

        page = req_params.get("page", 1)
        size = req_params.get("size", 1000)
        sort_by = req_params.get("sort_by", "meta.created")
        order_by = req_params.get("order_by", "desc")
        start_date = req_params.get("start_date", get_updated_time(days=-2).isoformat())
        end_date = req_params.get("end_date", get_current_time().isoformat())

        return {"status": SUCCESS, "message": "Audit events retrieved successfully ",
                "data": AUDIT_SERVICE.get_audits(page=page, size=size, sort_by=sort_by,
                                                 order_by=order_by, start_date=start_date, end_date=end_date)}
