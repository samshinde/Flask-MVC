from flask import request
from flask_jwt_extended import jwt_required
from flask_restplus import Resource, Namespace, marshal, abort, reqparse

from rest import api, auth_header_parser
from rest.stock.models import stock_request, stock_entity, stock_delete_request, stock_update_request
from rest.stock.service import StockService
from rest.common.base_models import response
from rest.common.constants import BAD_REQUEST, SUCCESS, STOCK_COLLECTION, FIELDS
from rest.common.schema_utils import must_not_be_blank, must_not_be_duplicate_value_for_field
from rest.common.utils import custom_marshal

stock_api_ns = Namespace('stock', description='stock operation')
# all_entity_api_ns = Namespace('entitys_hierarchy', description='list hierarchy of entities operation')

STOCK_SERVICE = StockService()

parser = reqparse.RequestParser()
parser.add_argument('filters', type=str, location='args')
parser.add_argument('search_query', type=str, location='args')

pagination_parser = reqparse.RequestParser()
pagination_parser.add_argument('page', type=str, location='args')
pagination_parser.add_argument('size', type=str, location='args')
pagination_parser.add_argument('sort_by', type=str, location='args')
pagination_parser.add_argument('order_by', type=str, location='args')



@api.expect(auth_header_parser)
@stock_api_ns.route('/<string:stock_type>')
class StockCollection(Resource):
    """
    Stock
    """

    @jwt_required
    @api.expect(pagination_parser)
    @api.marshal_with(response)
    def get(self, stock_type):
        """
        list entities
        :param stock_type
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
            search_dict = STOCK_SERVICE.get_search_dict(req_params.get('search_query'))
        else:
            search_dict = None

        if req_params.get('filters'):
            return {"status": SUCCESS,
                    "data": STOCK_SERVICE.filter_stocks(req_params.get('filters'), stock_type, search_dict, page,
                                                        size, sort_by,
                                                        order_by),
                    "message": "{} retrieved successfully".format(stock_type)}
        else:
            return {"status": SUCCESS,
                    "data": STOCK_SERVICE.get_stocks_by_type(stock_type, search_dict, page, size, sort_by,
                                                             order_by),
                    "message": "{} retrieved successfully".format(stock_type)}

    @jwt_required
    @api.expect(stock_request, validate=True)
    @api.marshal_with(response)
    def post(self, stock_type):
        """
        create stock
        :param: stock type
        :return: returns created stock
        """
        _parent = None
        request_data = request.get_json()

        stock_req_data = marshal(request_data, stock_request)

        if _parent:
            stock_req_data["parent_details"] = _parent

        data = custom_marshal(stock_req_data, stock_entity)
        return {"status": SUCCESS, "message": "{} added successfully".format(stock_type),
                "data": STOCK_SERVICE.create_stock(data, stock_type)}


@api.expect(auth_header_parser)
@stock_api_ns.route('/<string:stock_type>/<string:stock_id>')
class Stock(Resource):
    """
    Zone
    """

    @jwt_required
    @api.marshal_with(response)
    def get(self, stock_type, stock_id):
        """
        get entities
        :param stock_type
        :return: returns entities by id
        """
        return {"status": SUCCESS, "message": "{} retrieved successfully".format(stock_type),
                "data": STOCK_SERVICE.get_stock(stock_type, stock_id)}

    @jwt_required
    @api.expect(stock_request, validate=True)
    @api.marshal_with(response)
    def put(self, stock_type, stock_id):
        """
        update stock
        :param: stock_type
        :return: returns updated entities
        """
        request_data = marshal(request.get_json(), stock_update_request)
        return {"status": SUCCESS, "message": "{} updated successfully".format(stock_type),
                "data": STOCK_SERVICE.update_stock(request_data, stock_type, stock_id)}

    @jwt_required
    @api.marshal_with(response)
    def delete(self, stock_type, stock_id):
        """
        delete entities
        :param stock_type:
        :param stock_id: actual id of stock
        :return: returns message success / failure
        """
        # validate stock type
        stock = STOCK_SERVICE.get_stock_by_id(stock_id, raise_error=False)
        if not stock:
            abort(BAD_REQUEST, message="Invalid stock type : {}".format(stock_type), status=BAD_REQUEST)

        stock_name = stock.get("name") if stock else stock
        STOCK_SERVICE.delete_stock(stock_id)
        return {"status": SUCCESS, "message": "{} {} deleted successfully.".format(stock_type, stock_name)}


@api.expect(auth_header_parser)
@stock_api_ns.route('/<string:stock_type>/delete')
class DeleteStocks(Resource):
    @jwt_required
    @api.expect(stock_delete_request, validate=True)
    @api.marshal_with(response)
    def post(self, stock_type):
        """
        delete entities
        :param stock_type:
        :return: returns message success / failure
        """
        req_data = request.get_json()
        for stock_id in req_data["stock_ids"]:
            STOCK_SERVICE.delete_stock(stock_id)

        return {"status": SUCCESS, "message": "{} deleted successfully.".format(stock_type)}
