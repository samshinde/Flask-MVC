from flask import request
from flask_jwt_extended import jwt_required
from flask_restplus import Resource, Namespace, abort, reqparse

from rest import api, auth_header_parser
from rest.common.base_models import response
from rest.common.constants import BAD_REQUEST, SUCCESS
from rest.entity_types.models import entity_type, entity_type_request
from rest.entity_types.service import EntityTypeService
from rest.common.utils import custom_marshal

entity_type_api_ns = Namespace('entity_types', description='entity types operation')

ENTITY_TYPE_SERVICE = EntityTypeService()

parser = reqparse.RequestParser()
parser.add_argument('params', type=str, location='args')


@api.expect(auth_header_parser)
@entity_type_api_ns.route('/')
class EntityTypeCollection(Resource):
    """
    Entity Type Collection Operations
    """

    @jwt_required
    @api.marshal_with(response)
    def get(self):
        """
        list all entity types
        :return: returns entity types
        """
        return {"status": SUCCESS, "data": ENTITY_TYPE_SERVICE.get_all_entity_types(),
                "message": "entity types retrieved successfully"}

    @jwt_required
    @api.expect(entity_type_request, validate=True)
    @api.marshal_with(response)
    def post(self):
        """
        list all entity types
        :return: returns entity types
        """
        request_data = request.get_json()
        if not request_data:
            abort(BAD_REQUEST, message="Bad request data", status=BAD_REQUEST)

        data = custom_marshal(request_data, entity_type)
        return {"status": SUCCESS, "message": "entity type added successfully",
                "data": ENTITY_TYPE_SERVICE.create_entity_type(data)}


@api.expect(auth_header_parser)
@entity_type_api_ns.route('/<string:type_id>')
class EntityTypeItem(Resource):
    """
    Entity Type Item Operations
    """

    @jwt_required
    @api.marshal_with(response)
    def get(self, type_id):
        """
        get entity types
        :param type_id : Entity type id
        :return: returns entity type by id
        """
        return {"status": SUCCESS, "message": "entity type retrieved successfully",
                "data": ENTITY_TYPE_SERVICE.get_entity_type_by_id(type_id)}

    @jwt_required
    @api.expect(entity_type_request, validate=True)
    @api.marshal_with(response)
    def put(self, type_id):
        """
        update entity type
        :param: type_id
        :return: returns updated entity type
        """
        request_data = custom_marshal(request.get_json(), entity_type)
        return {"status": SUCCESS, "message": "entity type updated successfully",
                "data": ENTITY_TYPE_SERVICE.update_entity_type(request_data, type_id)}

    @jwt_required
    @api.marshal_with(response)
    def delete(self, type_id):
        """
        delete entity type
        :param type_id: actual id of entity type
        :return: returns message success / failure
        """
        ENTITY_TYPE_SERVICE.delete_entity_type(type_id)
        return {"status": SUCCESS, "message": "entity type deleted successfully."}
