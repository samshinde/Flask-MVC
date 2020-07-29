from flask import request
from flask_jwt_extended import jwt_required
from flask_restplus import Resource, Namespace, marshal, abort, reqparse

from rest import api, auth_header_parser
from rest.entities.models import entity_request, entity, entity_delete_request, entity_update_request
from rest.entities.service import EntityService
from rest.entity_types.service import EntityTypeService
from rest.common.base_models import response
from rest.common.constants import BAD_REQUEST, SUCCESS, ENTITY_COLLECTION, FIELDS
from rest.common.schema_utils import must_not_be_blank, must_not_be_duplicate_value_for_field
from rest.common.utils import custom_marshal
from rest.entities.templates.service import EntityTemplateService

entity_api_ns = Namespace('entities', description='entities operation')
all_entity_api_ns = Namespace('entitys_hierarchy', description='list hierarchy of entities operation')

ENTITY_SERVICE = EntityService()
ENTITY_TYPE_SERVICE = EntityTypeService()
TEMPLATE_SERVICE = EntityTemplateService()

parser = reqparse.RequestParser()
parser.add_argument('filters', type=str, location='args')
parser.add_argument('search_query', type=str, location='args')

pagination_parser = reqparse.RequestParser()
pagination_parser.add_argument('page', type=str, location='args')
pagination_parser.add_argument('size', type=str, location='args')
pagination_parser.add_argument('sort_by', type=str, location='args')
pagination_parser.add_argument('order_by', type=str, location='args')


@api.expect(auth_header_parser)
@all_entity_api_ns.route('/')
class ListEntityHierarchy(Resource):
    """
    Entitys hierarchy
    """

    @jwt_required
    @api.marshal_with(response)
    def get(self):
        """
        list entities in hierarchical manner
        :return:
        """
        return {"status": SUCCESS, "data": ENTITY_SERVICE.list_entitys_hierarchy(),
                "message": "entities retrieved successfully"}


@api.expect(auth_header_parser)
@all_entity_api_ns.route('/<string:entity_type>')
class ListEntityHierarchyByType(Resource):
    """
    Entitys hierarchy
    """

    @jwt_required
    @api.marshal_with(response)
    def get(self, entity_type):
        """
        list entities in hierarchical manner
        :return:
        """
        return {"status": SUCCESS, "data": ENTITY_SERVICE.list_entitys_hierarchy_by_type(entity_type),
                "message": "entities retrieved successfully"}


@api.expect(auth_header_parser)
@entity_api_ns.route('/<string:entity_type>')
class EntityCollection(Resource):
    """
    Entity
    """

    @jwt_required
    @api.expect(pagination_parser)
    @api.marshal_with(response)
    def get(self, entity_type):
        """
        list entities
        :param entity_type
        :return: list of entities depend on type
        """
        # validate entity type
        entity_type_obj = ENTITY_TYPE_SERVICE.get_entity_type_by_name(entity_type)
        if not entity_type_obj:
            abort(BAD_REQUEST, message="Invalid entity type : {}".format(entity_type), status=BAD_REQUEST)

        req_params = parser.parse_args(request)

        # remove None value from request
        req_params = {k: v for k, v in req_params.items() if v}

        page = req_params.get("page", 1)
        size = req_params.get("size", 1000)
        sort_by = req_params.get("sort_by", "name")
        order_by = req_params.get("order_by", "asc")

        if req_params.get('search_query'):
            search_dict = ENTITY_SERVICE.get_search_dict(req_params.get('search_query'))
        else:
            search_dict = None

        if req_params.get('filters'):
            return {"status": SUCCESS,
                    "data": ENTITY_SERVICE.filter_entitys(req_params.get('filters'), entity_type, search_dict, page,
                                                          size, sort_by,
                                                          order_by),
                    "message": "{} retrieved successfully".format(entity_type)}
        else:
            return {"status": SUCCESS,
                    "data": ENTITY_SERVICE.get_entitys_by_type(entity_type, search_dict, page, size, sort_by, order_by),
                    "message": "{} retrieved successfully".format(entity_type)}

    @jwt_required
    @api.expect(entity_request, validate=True)
    @api.marshal_with(response)
    def post(self, entity_type):
        """
        create entity
        :param: entity type
        :return: returns created entity
        """
        _parent = None
        request_data = request.get_json()

        # validate entity type
        entity_type_obj = ENTITY_TYPE_SERVICE.get_entity_type_by_name(entity_type)
        if not entity_type_obj:
            abort(BAD_REQUEST, message="Invalid entity type : {}".format(entity_type), status=BAD_REQUEST)

        # validate for parent other than base entity
        if entity_type not in ["default"]:
            parent_type = request_data.get('parent_type')
            parent_id = request_data.get('parent')

            # check parent entity
            must_not_be_blank(parent_type, 'parent_type')
            must_not_be_blank(parent_id, 'parent_id')

            _parent = ENTITY_SERVICE.get_entity(parent_type, parent_id)
            if not _parent:
                abort(BAD_REQUEST, message="Invalid parent entity: {}".format(parent_id), status=BAD_REQUEST)

        validate_entity_fields(entity_type, request_data)

        entity_req_data = marshal(request_data, entity_request)

        if _parent:
            entity_req_data["parent_details"] = _parent

        data = custom_marshal(entity_req_data, entity)
        return {"status": SUCCESS, "message": "{} added successfully".format(entity_type),
                "data": ENTITY_SERVICE.create_entity(data, entity_type_obj)}


@api.expect(auth_header_parser)
@entity_api_ns.route('/<string:entity_type>/<string:entity_id>')
class Entity(Resource):
    """
    Zone
    """

    @jwt_required
    @api.marshal_with(response)
    def get(self, entity_type, entity_id):
        """
        get entities
        :param entity_type
        :return: returns entities by id
        """
        return {"status": SUCCESS, "message": "{} retrieved successfully".format(entity_type),
                "data": ENTITY_SERVICE.get_entity(entity_type, entity_id)}

    @jwt_required
    @api.expect(entity_request, validate=True)
    @api.marshal_with(response)
    def put(self, entity_type, entity_id):
        """
        update entity
        :param: entity_type
        :return: returns updated entities
        """
        request_data = marshal(request.get_json(), entity_update_request)
        return {"status": SUCCESS, "message": "{} updated successfully".format(entity_type),
                "data": ENTITY_SERVICE.update_entity(request_data, entity_type, entity_id)}

    @jwt_required
    @api.marshal_with(response)
    def delete(self, entity_type, entity_id):
        """
        delete entities
        :param entity_type:
        :param entity_id: actual id of entity
        :return: returns message success / failure
        """
        # validate entity type
        entity = ENTITY_SERVICE.get_entity_by_id(entity_id, raise_error=False)
        if not entity:
            abort(BAD_REQUEST, message="Invalid entity type : {}".format(entity_type), status=BAD_REQUEST)

        entity_name = entity.get("name") if entity else entity
        ENTITY_SERVICE.delete_entity(entity_id)
        return {"status": SUCCESS, "message": "{} {} deleted successfully.".format(entity_type, entity_name)}


@api.expect(auth_header_parser)
@entity_api_ns.route('/<string:entity_type>/delete')
class DeleteEntitys(Resource):
    @jwt_required
    @api.expect(entity_delete_request, validate=True)
    @api.marshal_with(response)
    def post(self, entity_type):
        """
        delete entities
        :param entity_type:
        :return: returns message success / failure
        """
        req_data = request.get_json()
        for entity_id in req_data["entity_ids"]:
            ENTITY_SERVICE.delete_entity(entity_id)

        return {"status": SUCCESS, "message": "{} deleted successfully.".format(entity_type)}


def validate_entity_fields(entity_type, request_data):
    if entity_type:
        template = TEMPLATE_SERVICE.get_entity_template_by_entity_type(entity_type, raise_error=False)
    else:
        # raise error
        template = TEMPLATE_SERVICE.get_entity_template_by_entity_type(entity_type)

    if template:
        for field in template[FIELDS]:
            if field['is_required']:
                must_not_be_blank(request_data[FIELDS].get(field['key']), field['key'])
            if field["unique"]:
                must_not_be_duplicate_value_for_field(ENTITY_COLLECTION, entity_type, field['key'],
                                                      request_data[FIELDS].get(field['key']))
