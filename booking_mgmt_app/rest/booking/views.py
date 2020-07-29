from flask import request
from flask_jwt_extended import jwt_required
from flask_restplus import Resource, Namespace, marshal, abort, reqparse

from rest import api, auth_header_parser
from rest.booking.models import booking_request, booking_entity, booking_delete_request, booking_update_request
from rest.booking.service import BookingService
from rest.common.base_models import response
from rest.common.constants import BAD_REQUEST, SUCCESS, BOOKING_COLLECTION, FIELDS
from rest.common.schema_utils import must_not_be_blank, must_not_be_duplicate_value_for_field
from rest.common.utils import custom_marshal

booking_api_ns = Namespace('bookings', description='bookings operation')
# all_entity_api_ns = Namespace('entitys_hierarchy', description='list hierarchy of entities operation')

BOOKING_SERVICE = BookingService()

parser = reqparse.RequestParser()
parser.add_argument('filters', type=str, location='args')
parser.add_argument('search_query', type=str, location='args')

pagination_parser = reqparse.RequestParser()
pagination_parser.add_argument('page', type=str, location='args')
pagination_parser.add_argument('size', type=str, location='args')
pagination_parser.add_argument('sort_by', type=str, location='args')
pagination_parser.add_argument('order_by', type=str, location='args')


@api.expect(auth_header_parser)
@booking_api_ns.route('/<string:booking_type>')
class BookingCollection(Resource):
    """
    Booking
    """

    @jwt_required
    @api.expect(pagination_parser)
    @api.marshal_with(response)
    def get(self, booking_type):
        """
        list entities
        :param booking_type
        :return: list of entities depend on type
        """
        req_params = parser.parse_args(request)

        # remove None value from request
        req_params = {k: v for k, v in req_params.items() if v}

        page = req_params.get("page", 1)
        size = req_params.get("size", 1000)
        sort_by = req_params.get("sort_by", "name")
        order_by = req_params.get("order_by", "asc")

        if req_params.get('search_query'):
            search_dict = BOOKING_SERVICE.get_search_dict(req_params.get('search_query'))
        else:
            search_dict = None

        if req_params.get('filters'):
            return {"status": SUCCESS,
                    "data": BOOKING_SERVICE.filter_bookings(req_params.get('filters'), booking_type, search_dict, page,
                                                            size, sort_by,
                                                            order_by),
                    "message": "{} retrieved successfully".format(booking_type)}
        else:
            return {"status": SUCCESS,
                    "data": BOOKING_SERVICE.get_bookings_by_type(booking_type, search_dict, page, size, sort_by,
                                                                 order_by),
                    "message": "{} retrieved successfully".format(booking_type)}

    @jwt_required
    @api.expect(booking_request, validate=True)
    @api.marshal_with(response)
    def post(self, booking_type):
        """
        create booking
        :param: booking type
        :return: returns created booking
        """
        _parent = None
        request_data = request.get_json()

        booking_req_data = marshal(request_data, booking_request)

        if _parent:
            booking_req_data["parent_details"] = _parent

        data = custom_marshal(booking_req_data, booking_entity)
        return {"status": SUCCESS, "message": "{} added successfully".format(booking_type),
                "data": BOOKING_SERVICE.create_booking(data, booking_type)}


@api.expect(auth_header_parser)
@booking_api_ns.route('/<string:booking_type>/<string:booking_id>')
class Booking(Resource):
    """
    Zone
    """

    @jwt_required
    @api.marshal_with(response)
    def get(self, booking_type, booking_id):
        """
        get entities
        :param booking_type
        :return: returns entities by id
        """
        return {"status": SUCCESS, "message": "{} retrieved successfully".format(booking_type),
                "data": BOOKING_SERVICE.get_booking(booking_type, booking_id)}

    @jwt_required
    @api.expect(booking_request, validate=True)
    @api.marshal_with(response)
    def put(self, booking_type, booking_id):
        """
        update booking
        :param: booking_type
        :return: returns updated entities
        """
        request_data = marshal(request.get_json(), booking_update_request)
        return {"status": SUCCESS, "message": "{} updated successfully".format(booking_type),
                "data": BOOKING_SERVICE.update_booking(request_data, booking_type, booking_id)}

    @jwt_required
    @api.marshal_with(response)
    def delete(self, booking_type, booking_id):
        """
        delete entities
        :param booking_type:
        :param booking_id: actual id of booking
        :return: returns message success / failure
        """
        # validate booking type
        booking = BOOKING_SERVICE.get_booking_by_id(booking_id, raise_error=False)
        if not booking:
            abort(BAD_REQUEST, message="Invalid booking type : {}".format(booking_type), status=BAD_REQUEST)

        booking_name = booking.get("name") if booking else booking
        BOOKING_SERVICE.delete_booking(booking_id)
        return {"status": SUCCESS, "message": "{} {} deleted successfully.".format(booking_type, booking_name)}


@api.expect(auth_header_parser)
@booking_api_ns.route('/<string:booking_type>/delete')
class DeleteBookings(Resource):
    @jwt_required
    @api.expect(booking_delete_request, validate=True)
    @api.marshal_with(response)
    def post(self, booking_type):
        """
        delete entities
        :param booking_type:
        :return: returns message success / failure
        """
        req_data = request.get_json()
        for booking_id in req_data["booking_ids"]:
            BOOKING_SERVICE.delete_booking(booking_id)

        return {"status": SUCCESS, "message": "{} deleted successfully.".format(booking_type)}
