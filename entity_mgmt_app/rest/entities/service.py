from bson import ObjectId
from flask_restplus import abort, marshal

from rest.entities.models import entity_response, entity_hierarchy_response
from rest.common.constants import ENTITY_COLLECTION, NAME, ID, PARENT_DETAILS, PARENT_TYPE
from rest.common.constants import META, IS_DELETED, ENTITY_TYPE, ENTITY_TYPE_DETAILS, PARENT, UPDATED, \
    INTERNAL_SERVER_ERROR, \
    ENTITY_NOT_FOUND, ENTITY_ALREADY_EXISTS
from rest.utils.dateutils import get_current_time
from rest.utils.db_service import Base


class EntityService(Base):
    def create_entity(self, req_data, entity_type_obj):
        """
        create entities
        :param req_data:
        :param entity_type_obj:
        :return:
        """
        _count, _entity = self.get(ENTITY_COLLECTION,
                                   {f"{META}.{IS_DELETED}": False,
                                   NAME: req_data[NAME],
                                   ENTITY_TYPE: entity_type_obj.get('name')})

        if _count == 1 and _entity:
            abort(ENTITY_ALREADY_EXISTS, message="Entity already exists with given name.", status=ENTITY_ALREADY_EXISTS)

        req_data[ENTITY_TYPE] = entity_type_obj.get('name')
        req_data[ENTITY_TYPE_DETAILS] = entity_type_obj

        if req_data.get(PARENT):
            req_data[PARENT] = ObjectId(req_data.get(PARENT))

        result, _id = self.create(ENTITY_COLLECTION, req_data)

        if result:
            req_data[ID] = _id
            return marshal(req_data, entity_response)
        else:
            abort(INTERNAL_SERVER_ERROR, message='Error in inserting records to {} collection'.format(ENTITY_COLLECTION),
                  status=INTERNAL_SERVER_ERROR)

    def get_entitys_by_type(self, entity_type, search_dict=None, page=1, size=1000, sort_by="name", order_by="asc"):
        """
        get all entities
        :param entity_type:
        :param search_dict:
        :param page:
        :param size:
        :param sort_by:
        :param order_by:
        :return: list entities by entity type
        """
        query_dict = {f"{META}.{IS_DELETED}": False,
                 ENTITY_TYPE: entity_type}

        if search_dict is not None:
            query_dict.update(search_dict)

        _count, _entitys = self.get(ENTITY_COLLECTION,
                                    query_dict,
                                    sort_by=sort_by,
                                    order_by=order_by,
                                    page=page,
                                    size=size)
        return {'records': marshal(_entitys, entity_response), 'count': _count}

    def filter_entitys(self, query_params, entity_type, search_dict=None, page=1, size=1000, sort_by="name", order_by="asc"):
        """
        apply query params to aggregate query
        :param query_params:
        :param entity_type:
        :param search_dict:
        :param page:
        :param size:
        :param sort_by:
        :param order_by:
        :return:
        """
        query_dict = {f'{META}.{IS_DELETED}': False,
                      ENTITY_TYPE: entity_type}

        if search_dict is not None:
            query_dict.update(search_dict)

        if isinstance(query_params, str) and "&" in query_params:
            for filter_item in query_params.split('&'):
                query_dict[filter_item.split('=')[0]] = filter_item.split('=')[1]
        elif isinstance(query_params, dict):
            query_dict.update(query_params)

        _count, _entitys = self.get(ENTITY_COLLECTION,
                                    query_dict,
                                    sort_by=sort_by,
                                    order_by=order_by,
                                    page=page,
                                    size=size)
        return {'records': marshal(_entitys, entity_response), 'count': _count}

    def get_search_dict(self, search_query):
        """
        create search query
        :param search_query:
        :return:
        """

        search_dict = {}

        if isinstance(search_query, str):
            for search_item in search_query.split(","):
                search_dict[search_query.split(":")[0]] = {"$regex": search_item.split(":")[1], "$options": "i"}
        elif isinstance(search_query, dict):
            search_dict.update(search_query)

        return search_dict

    def get_entitys_by_name(self, entity_name, entity_type=None, raise_error=True):
        """
        get entity
        :param entity_name
        :param entity_type
        :param raise_error
        :return: get entity by name
        """
        if entity_type:
            _count, _entity = self.get(ENTITY_COLLECTION, {f"{META}.{IS_DELETED}": False,
                                                         "name": entity_name,
                                                           ENTITY_TYPE:entity_type})
        else:
            _count, _entity = self.get(ENTITY_COLLECTION, {f"{META}.{IS_DELETED}": False,
                                                         "name": entity_name})
        if _count == 1 and _entity:
            return marshal(_entity[0], entity_response)
        elif raise_error:
            abort(ENTITY_NOT_FOUND, message="Entity with name {} does not exists.".format(entity_name),
                  status=ENTITY_NOT_FOUND)
        else:
            return None

    def get_entity(self, entity_type, entity_id, raise_error=True):
        """
        get entities by _id
        :param entity_type
        :param entity_id:
        :return:
        """
        _count, _entity = self.get(ENTITY_COLLECTION, {f"{META}.{IS_DELETED}": False,
                                                       ID: ObjectId(entity_id),
                                                       ENTITY_TYPE: entity_type})
        if _count == 1 and _entity:
            return marshal(_entity[0], entity_response)
        elif raise_error:
            abort(ENTITY_NOT_FOUND, message="entity {} with {} does not exists.".format(entity_type, entity_id),
                  status=ENTITY_NOT_FOUND)
        else:
            return None

    def get_entity_by_id(self, entity_id, raise_error=True):
        """
        get entities by _id
        :param entity_type
        :param entity_id:
        :return:
        """
        _count, _entity = self.get(ENTITY_COLLECTION, {f"{META}.{IS_DELETED}": False,
                                                       ID: ObjectId(entity_id)})
        if _count == 1 and _entity:
            return marshal(_entity[0], entity_response)
        elif raise_error:
            abort(ENTITY_NOT_FOUND, message="Entity with ID : {} does not exists.".format(entity_id),
                  status=ENTITY_NOT_FOUND)
        else:
            return None

    def update_entity(self, req_data, entity_type, entity_id):
        """
        update entities
        :param req_data:
        :param entity_type
        :param entity_id:
        :return:
        """
        _entity = self.get_entity(entity_type, entity_id)
        if _entity:
            req_data[META] = _entity[META]
            req_data[META][UPDATED] = get_current_time()

            if req_data.get(PARENT):
                parent = self.get_entity(req_data.get(PARENT_TYPE), req_data.get(PARENT))
                req_data[PARENT_DETAILS] = parent

            self.update(ENTITY_COLLECTION,
                        query={f"{META}.{IS_DELETED}": False, ID: ObjectId(entity_id)},
                        updated_record=req_data)

            entity = self.get_entity(entity_type, entity_id)
            self.update(ENTITY_COLLECTION,
                        query={f"{META}.{IS_DELETED}": False,
                               f"{PARENT_DETAILS}.{ID}": entity_id},
                        updated_record={PARENT_DETAILS: entity},
                        multi=True)
        else:
            abort(ENTITY_NOT_FOUND,
                  message="Entity {} with id {} doesn't exists to update".format(entity_type, entity_id),
                  status=ENTITY_NOT_FOUND)

        return entity

    def delete_entity(self, entity_id):
        """
        delete entities by _id
        :param entity_id:
        :return:
        """
        self.update(ENTITY_COLLECTION, query={ID: ObjectId(entity_id)},
                    update_query={"$set": {f"{META}.{IS_DELETED}": True}})

    def list_entitys_hierarchy(self):
        lookup_query = [{'$match': {f'{META}.{IS_DELETED}': False}},
                        {'$graphLookup': {'connectToField': '_id', 'connectFromField': 'parent',
                                          'from': ENTITY_COLLECTION, 'startWith':
                                              '$parent', 'as': 'hierarchy'}}]
        _count, _records = self.aggregate(ENTITY_COLLECTION, lookup_query)
        return {'records': marshal(_records, entity_hierarchy_response), 'count': _count}

    def list_entitys_hierarchy_by_type(self, entity_type):
        """
        list entities hierarchy by type
        :param entity_type:
        :return:
        """
        lookup_query = [{'$match': {f"{META}.{IS_DELETED}": False, ENTITY_TYPE: entity_type}},
                        {'$graphLookup': {'connectToField': '_id', 'connectFromField': 'parent',
                                          'from': ENTITY_COLLECTION, 'startWith': '$parent', 'as': 'hierarchy'}}]

        _count, _entitys = self.aggregate(ENTITY_COLLECTION, lookup_query)
        return {'records': marshal(_entitys, entity_hierarchy_response), 'count': _count}

    def filter_entitys_hierarchy(self, query_params, entity_type):
        """
        apply query params to aggregate query
        :param query_params:
        :return:
        """
        query_dict = {f'{META}.{IS_DELETED}': False, ENTITY_TYPE: entity_type}
        for filter_item in query_params.split('&'):
            query_dict[filter_item.split('=')[0]] = filter_item.split('=')[1]

        lookup_query = [{'$match': query_dict},
                        {'$graphLookup': {'connectToField': '_id', 'connectFromField': 'parent',
                                          'from': ENTITY_COLLECTION, 'startWith':
                                              '$parent', 'as': 'hierarchy'}}]
        _count, _records = self.aggregate(ENTITY_COLLECTION, lookup_query)
        return {'records': marshal(_records, entity_hierarchy_response), 'count': _count}
