from bson import ObjectId
from flask_restplus import abort, marshal

from rest.entities.models import set_bson_object
from rest.common.constants import ENTITY_TYPE_COLLECTION, NAME, ID
from rest.common.constants import META, IS_DELETED, UPDATED, INTERNAL_SERVER_ERROR, \
    ENTITY_NOT_FOUND, ENTITY_ALREADY_EXISTS
from rest.entity_types.models import entity_type_response
from rest.utils.dateutils import get_current_time
from rest.utils.db_service import Base


class EntityTypeService(Base):
    """
    Entity Type Service
    """

    def create_entity_type(self, req_data):
        """
        create entity_types
        :param req_data:
        :param entity_type:
        :return:
        """
        _count, _entity_type = self.get(ENTITY_TYPE_COLLECTION,
                                        {f"{META}.{IS_DELETED}": False,
                                         NAME: req_data[NAME]})

        if _count == 1 and _entity_type:
            abort(ENTITY_ALREADY_EXISTS, message="Entity Type already exists with given name.",
                  status=ENTITY_ALREADY_EXISTS)

        result, _id = self.create(ENTITY_TYPE_COLLECTION, req_data)

        if result:
            req_data = set_bson_object(req_data, ID, _id)
            return marshal(req_data, entity_type_response)
        else:
            abort(INTERNAL_SERVER_ERROR,
                  message='Error in inserting records to {} collection'.format(ENTITY_TYPE_COLLECTION),
                  status=INTERNAL_SERVER_ERROR)

    def get_all_entity_types(self):
        """
        get all entity_types
        :return: list entity_types by entity_type
        """
        _count, _entity_types = self.get(ENTITY_TYPE_COLLECTION, {f"{META}.{IS_DELETED}": False})
        return {'records': marshal(_entity_types, entity_type_response), 'count': _count}

    def get_entity_type_by_id(self, entity_type_id):
        """
        get entity_types by _id
        :param entity_type_id:
        :return:
        """
        _count, _entity_type = self.get(ENTITY_TYPE_COLLECTION, {f"{META}.{IS_DELETED}": False,
                                                                 ID: ObjectId(entity_type_id)})
        if _count >= 1 and _entity_type:
            return marshal(_entity_type[0], entity_type_response)
        else:
            abort(ENTITY_NOT_FOUND, message="entity with ID {} does not exists.".format(entity_type_id),
                  status=ENTITY_NOT_FOUND)

    def get_entity_type_by_name(self, entity_type):
        """
        get entity_types by _id
        :param entity_type_id:
        :return:
        """
        _count, _entity_type = self.get(ENTITY_TYPE_COLLECTION, {f"{META}.{IS_DELETED}": False,
                                                                 'name': entity_type})
        if _count >= 1 and _entity_type:
            return marshal(_entity_type[0], entity_type_response)
        else:
            abort(ENTITY_NOT_FOUND, message="Entity with name {} does not exists.".format(entity_type),
                  status=ENTITY_NOT_FOUND)

    def update_entity_type(self, req_data, entity_type_id):
        """
        update entity_types
        :param req_data:
        :param entity_type_id:
        :return:
        """
        _entity_type = self.get_entity_type_by_id(entity_type_id)
        if _entity_type:
            req_data[META] = _entity_type[META]
            req_data[META][UPDATED] = get_current_time()
            # TODO updated by
            self.update(ENTITY_TYPE_COLLECTION,
                        query={f"{META}.{IS_DELETED}": False, ID: ObjectId(entity_type_id)},
                        updated_record=req_data)
        else:
            abort(ENTITY_NOT_FOUND,
                  message="Entity with id {} doesn't exists to update".format(entity_type_id),
                  status=ENTITY_NOT_FOUND)

        return self.get_entity_type_by_id(entity_type_id)

    def delete_entity_type(self, entity_type_id):
        """
        delete entity_types by _id
        :param entity_type_id:
        :return:
        """
        self.update(ENTITY_TYPE_COLLECTION, query={ID: ObjectId(entity_type_id)},
                    update_query={"$set": {f"{META}.{IS_DELETED}": True}})
