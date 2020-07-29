from bson import ObjectId
from flask_restplus import abort, marshal

from rest.entities.templates.models import entity_template_response
from rest.entities.models import set_bson_object
from rest.common.constants import ENTITY_TEMPLATE_COLLECTION, ID
from rest.common.constants import META, IS_DELETED, UPDATED, INTERNAL_SERVER_ERROR, \
    ENTITY_NOT_FOUND, ENTITY_ALREADY_EXISTS, ENTITY_TYPE, ENTITY_TYPE_DETAILS
from rest.utils.dateutils import get_current_time
from rest.utils.db_service import Base
from rest.entities.service import EntityService

ASSET_SERVICE = EntityService()


class EntityTemplateService(Base):
    """
    AssetTemplate Type Service
    """

    def create_entity_template(self, req_data, entity_type_obj):
        """
        create templates
        :param req_data:
        :param entity_type_obj:
        :return: created entity template
        """
        _count, _entity_template = self.get(ENTITY_TEMPLATE_COLLECTION,
                                            {f"{META}.{IS_DELETED}": False,
                                             ENTITY_TYPE: entity_type_obj.get('name')})

        if _count == 1 and _entity_template:
            abort(ENTITY_ALREADY_EXISTS, message="Asset template already exists with given name.",
                  status=ENTITY_ALREADY_EXISTS)

        req_data[ENTITY_TYPE] = entity_type_obj.get('name')
        req_data[ENTITY_TYPE_DETAILS] = entity_type_obj
        _result, _id = self.create(ENTITY_TEMPLATE_COLLECTION, req_data)

        if _result:
            req_data = set_bson_object(req_data, ID, _id)
            return marshal(req_data, entity_template_response)
        else:
            abort(INTERNAL_SERVER_ERROR,
                  message='Error in inserting records to {} collection'.format(ENTITY_TEMPLATE_COLLECTION),
                  status=INTERNAL_SERVER_ERROR)

    def get_all_entity_templates(self):
        """
        get all templates
        :return: list templates by entity
        """
        _count, _entity_templates = self.get(ENTITY_TEMPLATE_COLLECTION, {f"{META}.{IS_DELETED}": False})
        return {'records': marshal(_entity_templates, entity_template_response), 'count': _count}

    def get_all_entity_templates_by_entity(self, entity_type):
        """
        list all entity templates by entity
        :param entity_type:
        :return:
        """
        _count, _entity_templates = self.get(ENTITY_TEMPLATE_COLLECTION,
                                             {f"{META}.{IS_DELETED}": False, ENTITY_TYPE: entity_type})
        return {'records': marshal(_entity_templates, entity_template_response), 'count': _count}

    def get_entity_template_by_id(self, entity_type, entity_template_id):
        """
        get templates by _id
        :param entity_type
        :param entity_template_id:
        :return:
        """
        _count, _entity_template = self.get(ENTITY_TEMPLATE_COLLECTION, {f"{META}.{IS_DELETED}": False,
                                                                         ENTITY_TYPE: entity_type,
                                                                         ID: ObjectId(entity_template_id)})
        if _count == 1 and _entity_template:
            return marshal(_entity_template[0], entity_template_response)
        else:
            abort(ENTITY_NOT_FOUND, message="Asset templates with ID {} does not exists.".format(entity_template_id),
                  status=ENTITY_NOT_FOUND)

    def get_entity_template_by_entity_type(self, entity_type, raise_error=True):
        """
        get templates by _id
        :param entity_type
        :return:
        """
        _count, _entity_template = self.get(ENTITY_TEMPLATE_COLLECTION, {f"{META}.{IS_DELETED}": False,
                                                                         ENTITY_TYPE: entity_type})
        if _count == 1 and _entity_template:
            return marshal(_entity_template[0], entity_template_response)
        elif raise_error:
            abort(ENTITY_NOT_FOUND, message="Asset templates for entity type {} does not exists.".format(entity_type),
                  status=ENTITY_NOT_FOUND)
        else:
            return None

    def update_entity_template(self, req_data, entity_template_id):
        """
        update templates
        :param req_data:
        :param entity_template_id:
        :return:
        """
        _entity_template = self.get_entity_template_by_id(req_data.get('entity_type'), entity_template_id)
        if _entity_template:

            if not req_data.get('force'):
                # check if user is removing the field which already having some value for any entity.
                self.validate_field_updates(req_data.get('entity_type'), _entity_template.get('fields'),
                                            req_data.get('fields'))

            req_data[META] = _entity_template[META]
            req_data[META][UPDATED] = get_current_time()
            self.update(ENTITY_TEMPLATE_COLLECTION,
                        query={f"{META}.{IS_DELETED}": False, ID: ObjectId(entity_template_id)},
                        updated_record=req_data)

            # TODO : remove fields from all entity fields too

        else:
            abort(ENTITY_NOT_FOUND,
                  message="Asset templates with id {} doesn't exists to update".format(entity_template_id),
                  status=ENTITY_NOT_FOUND)

        return self.get_entity_template_by_id(req_data.get('entity_type'), entity_template_id)

    def validate_field_updates(self, entity_type, original_fields, fields_to_be_updated):
        """
        Check or Cross verify fields to be removed from templates.
        :param entity_type:
        :param original_fields:
        :param fields_to_be_updated
        :return:
        """
        updated_keys = self.diff_lists(original_fields, fields_to_be_updated)
        for key in updated_keys:
            # filter entities
            _filtered_entitys = ASSET_SERVICE.filter_entitys({f"fields.{key}": {'$exists': True, '$ne': ''}},
                                                             entity_type)
            if _filtered_entitys.get('count') > 0:
                abort(INTERNAL_SERVER_ERROR, message=f"Fields trying to remove is already used in \
                entitys : {[i.get('name') for i in _filtered_entitys.get('records')]}", status=INTERNAL_SERVER_ERROR)

    def diff_lists(self, li1, li2):
        """
        diff of two lists
        :param li1:
        :param li2:
        :return:
        """
        li_dif = list({dict2['key'] for dict2 in li1} - {dict1['key'] for dict1 in li2})
        return li_dif

    def delete_entity_template(self, entity_template_id):
        """
        delete templates by _id
        :param entity_template_id:
        :return:
        """
        self.update(ENTITY_TEMPLATE_COLLECTION, query={ID: ObjectId(entity_template_id)},
                    update_query={"$set": {f"{META}.{IS_DELETED}": True}})
