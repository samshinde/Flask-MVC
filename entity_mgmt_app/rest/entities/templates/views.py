from flask import request
from flask_restplus import Resource, Namespace, abort, reqparse

from rest import api
from rest.entities.templates.models import entity_template, entity_template_request
from rest.entities.templates.service import EntityTemplateService
from rest.common.base_models import response
from rest.common.constants import BAD_REQUEST, SUCCESS
from rest.entity_types.service import EntityTypeService
from rest.common.utils import custom_marshal

entity_template_api_ns = Namespace('templates', description='entity templates operation')

ASSET_TEMPLATE_SERVICE = EntityTemplateService()
ENTITY_TYPE_SERVICE = EntityTypeService()

parser = reqparse.RequestParser()
parser.add_argument('params', type=str, location='args')


@entity_template_api_ns.route('/<string:entity_type>')
class AssetTemplateCollection(Resource):
    """
    entity template Collection Operations
    """

    @api.marshal_with(response)
    def get(self, entity_type):
        """
        list all entity templates
        :return: returns entity templates
        """
        return {"status": SUCCESS, "data": ASSET_TEMPLATE_SERVICE.get_all_entity_templates_by_entity(entity_type),
                "message": "entity templates retrieved successfully"}

    @api.expect(entity_template_request, validate=True)
    @api.marshal_with(response)
    def post(self, entity_type):
        """
        create entity templates
        :return: returns created entity templates
        """
        request_data = request.get_json()
        if not request_data:
            abort(BAD_REQUEST, message="Bad request data", status=BAD_REQUEST)

        # validate entity type
        entity_type_obj = ENTITY_TYPE_SERVICE.get_entity_type_by_name(entity_type)
        if not entity_type_obj:
            abort(BAD_REQUEST, message="Invalid entity type : {}".format(entity_type), status=BAD_REQUEST)

        data = custom_marshal(request_data, entity_template)
        return {"status": SUCCESS, "message": "entity template added successfully",
                "data": ASSET_TEMPLATE_SERVICE.create_entity_template(data, entity_type_obj)}


@entity_template_api_ns.route('/<string:entity_type>/<string:template_id>')
class AssetTemplateItem(Resource):
    """
    entity template Item Operations
    """

    @api.marshal_with(response)
    def get(self, entity_type, template_id):
        """
        get entity templates
        :param entity_type : entity type
        :param template_id : entity template id
        :return: returns entity template by id
        """
        # validate entity type
        entity_type_obj = ENTITY_TYPE_SERVICE.get_entity_type_by_name(entity_type)
        if not entity_type_obj:
            abort(BAD_REQUEST, message="Invalid entity type : {}".format(entity_type), status=BAD_REQUEST)

        return {"status": SUCCESS, "message": "entity template retrieved successfully",
                "data": ASSET_TEMPLATE_SERVICE.get_entity_template_by_id(entity_type, template_id)}

    @api.expect(entity_template_request, validate=True)
    @api.marshal_with(response)
    def put(self, entity_type, template_id):
        """
        update entity template
        :param entity_type
        :param: template_id
        :return: returns updated entity template
        """
        # validate entity type
        entity_type_obj = ENTITY_TYPE_SERVICE.get_entity_type_by_name(entity_type)
        if not entity_type_obj:
            abort(BAD_REQUEST, message="Invalid entity type : {}".format(entity_type), status=BAD_REQUEST)

        request_data = custom_marshal(request.get_json(), entity_template)
        return {"status": SUCCESS, "message": "entity template updated successfully",
                "data": ASSET_TEMPLATE_SERVICE.update_entity_template(request_data, template_id)}

    @api.marshal_with(response)
    def delete(self, entity_type, template_id):
        """
        delete entity template
        :param entity_type:
        :param template_id: actual id of entity template
        :return: returns message success / failure
        """
        # validate entity type
        entity_type_obj = ENTITY_TYPE_SERVICE.get_entity_type_by_name(entity_type)
        if not entity_type_obj:
            abort(BAD_REQUEST, message="Invalid entity type : {}".format(entity_type), status=BAD_REQUEST)

        ASSET_TEMPLATE_SERVICE.delete_entity_template(template_id)
        return {"status": SUCCESS, "message": "entity template deleted successfully."}
