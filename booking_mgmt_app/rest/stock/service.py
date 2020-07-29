from bson import ObjectId
from flask_restplus import abort, marshal

from rest.stock.models import stock_response
from rest.common.constants import STOCK_COLLECTION, NAME, ID, PARENT_DETAILS, PARENT_TYPE
from rest.common.constants import META, IS_DELETED, ENTITY_TYPE, ENTITY_TYPE_DETAILS, PARENT, UPDATED, \
    INTERNAL_SERVER_ERROR, \
    ENTITY_NOT_FOUND, ENTITY_ALREADY_EXISTS
from rest.utils.dateutils import get_current_time
from rest.utils.db_service import Base


class StockService(Base):
    def create_stock(self, req_data, stock_type_obj):
        """
        create entities
        :param req_data:
        :param stock_type_obj:
        :return:
        """
        _count, _stock = self.get(STOCK_COLLECTION,
                                  {f"{META}.{IS_DELETED}": False,
                                   NAME: req_data[NAME],
                                   ENTITY_TYPE: stock_type_obj.get('name')})

        if _count == 1 and _stock:
            abort(ENTITY_ALREADY_EXISTS, message="Entity already exists with given name.", status=ENTITY_ALREADY_EXISTS)

        req_data[ENTITY_TYPE] = stock_type_obj.get('name')
        req_data[ENTITY_TYPE_DETAILS] = stock_type_obj

        if req_data.get(PARENT):
            req_data[PARENT] = ObjectId(req_data.get(PARENT))

        result, _id = self.create(STOCK_COLLECTION, req_data)

        if result:
            req_data[ID] = _id
            return marshal(req_data, stock_response)
        else:
            abort(INTERNAL_SERVER_ERROR, message='Error in inserting records to {} collection'.format(STOCK_COLLECTION),
                  status=INTERNAL_SERVER_ERROR)

    def get_stocks_by_type(self, stock_type, search_dict=None, page=1, size=1000, sort_by="name", order_by="asc"):
        """
        get all entities
        :param stock_type:
        :param search_dict:
        :param page:
        :param size:
        :param sort_by:
        :param order_by:
        :return: list entities by stock type
        """
        query_dict = {f"{META}.{IS_DELETED}": False,
                      ENTITY_TYPE: stock_type}

        if search_dict is not None:
            query_dict.update(search_dict)

        _count, _stocks = self.get(STOCK_COLLECTION,
                                   query_dict,
                                   sort_by=sort_by,
                                   order_by=order_by,
                                   page=page,
                                   size=size)
        return {'records': marshal(_stocks, stock_response), 'count': _count}

    def filter_stocks(self, query_params, stock_type, search_dict=None, page=1, size=1000, sort_by="name",
                      order_by="asc"):
        """
        apply query params to aggregate query
        :param query_params:
        :param stock_type:
        :param search_dict:
        :param page:
        :param size:
        :param sort_by:
        :param order_by:
        :return:
        """
        query_dict = {f'{META}.{IS_DELETED}': False,
                      ENTITY_TYPE: stock_type}

        if search_dict is not None:
            query_dict.update(search_dict)

        if isinstance(query_params, str) and "&" in query_params:
            for filter_item in query_params.split('&'):
                query_dict[filter_item.split('=')[0]] = filter_item.split('=')[1]
        elif isinstance(query_params, dict):
            query_dict.update(query_params)

        _count, _stocks = self.get(STOCK_COLLECTION,
                                   query_dict,
                                   sort_by=sort_by,
                                   order_by=order_by,
                                   page=page,
                                   size=size)
        return {'records': marshal(_stocks, stock_response), 'count': _count}

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

    def get_stocks_by_name(self, stock_name, stock_type=None, raise_error=True):
        """
        get stock
        :param stock_name
        :param stock_type
        :param raise_error
        :return: get stock by name
        """
        if stock_type:
            _count, _stock = self.get(STOCK_COLLECTION, {f"{META}.{IS_DELETED}": False,
                                                         "name": stock_name,
                                                         ENTITY_TYPE: stock_type})
        else:
            _count, _stock = self.get(STOCK_COLLECTION, {f"{META}.{IS_DELETED}": False,
                                                         "name": stock_name})
        if _count == 1 and _stock:
            return marshal(_stock[0], stock_response)
        elif raise_error:
            abort(ENTITY_NOT_FOUND, message="Entity with name {} does not exists.".format(stock_name),
                  status=ENTITY_NOT_FOUND)
        else:
            return None

    def get_stock(self, stock_type, stock_id, raise_error=True):
        """
        get entities by _id
        :param stock_type
        :param stock_id:
        :return:
        """
        _count, _stock = self.get(STOCK_COLLECTION, {f"{META}.{IS_DELETED}": False,
                                                     ID: ObjectId(stock_id),
                                                     ENTITY_TYPE: stock_type})
        if _count == 1 and _stock:
            return marshal(_stock[0], stock_response)
        elif raise_error:
            abort(ENTITY_NOT_FOUND, message="stock {} with {} does not exists.".format(stock_type, stock_id),
                  status=ENTITY_NOT_FOUND)
        else:
            return None

    def get_stock_by_id(self, stock_id, raise_error=True):
        """
        get entities by _id
        :param stock_type
        :param stock_id:
        :return:
        """
        _count, _stock = self.get(STOCK_COLLECTION, {f"{META}.{IS_DELETED}": False,
                                                     ID: ObjectId(stock_id)})
        if _count == 1 and _stock:
            return marshal(_stock[0], stock_response)
        elif raise_error:
            abort(ENTITY_NOT_FOUND, message="Entity with ID : {} does not exists.".format(stock_id),
                  status=ENTITY_NOT_FOUND)
        else:
            return None

    def update_stock(self, req_data, stock_type, stock_id):
        """
        update entities
        :param req_data:
        :param stock_type
        :param stock_id:
        :return:
        """
        _stock = self.get_stock(stock_type, stock_id)
        if _stock:
            req_data[META] = _stock[META]
            req_data[META][UPDATED] = get_current_time()

            if req_data.get(PARENT):
                parent = self.get_stock(req_data.get(PARENT_TYPE), req_data.get(PARENT))
                req_data[PARENT_DETAILS] = parent

            self.update(STOCK_COLLECTION,
                        query={f"{META}.{IS_DELETED}": False, ID: ObjectId(stock_id)},
                        updated_record=req_data)

            _stock = self.get_stock(stock_type, stock_id)
            self.update(STOCK_COLLECTION,
                        query={f"{META}.{IS_DELETED}": False,
                               f"{PARENT_DETAILS}.{ID}": stock_id},
                        updated_record={PARENT_DETAILS: _stock},
                        multi=True)
        else:
            abort(ENTITY_NOT_FOUND,
                  message="Entity {} with id {} doesn't exists to update".format(stock_type, stock_id),
                  status=ENTITY_NOT_FOUND)

        return _stock

    def delete_stock(self, stock_id):
        """
        delete entities by _id
        :param stock_id:
        :return:
        """
        self.update(STOCK_COLLECTION, query={ID: ObjectId(stock_id)},
                    update_query={"$set": {f"{META}.{IS_DELETED}": True}})

    # def list_stocks_hierarchy(self):
    #     lookup_query = [{'$match': {f'{META}.{IS_DELETED}': False}},
    #                     {'$graphLookup': {'connectToField': '_id', 'connectFromField': 'parent',
    #                                       'from': STOCK_COLLECTION, 'startWith':
    #                                           '$parent', 'as': 'hierarchy'}}]
    #     _count, _records = self.aggregate(STOCK_COLLECTION, lookup_query)
    #     return {'records': marshal(_records, stock_hierarchy_response), 'count': _count}
    #
    # def list_stocks_hierarchy_by_type(self, stock_type):
    #     """
    #     list entities hierarchy by type
    #     :param stock_type:
    #     :return:
    #     """
    #     lookup_query = [{'$match': {f"{META}.{IS_DELETED}": False, ENTITY_TYPE: stock_type}},
    #                     {'$graphLookup': {'connectToField': '_id', 'connectFromField': 'parent',
    #                                       'from': STOCK_COLLECTION, 'startWith': '$parent', 'as': 'hierarchy'}}]
    #
    #     _count, _stocks = self.aggregate(STOCK_COLLECTION, lookup_query)
    #     return {'records': marshal(_stocks, stock_hierarchy_response), 'count': _count}
    #
    # def filter_stocks_hierarchy(self, query_params, stock_type):
    #     """
    #     apply query params to aggregate query
    #     :param query_params:
    #     :return:
    #     """
    #     query_dict = {f'{META}.{IS_DELETED}': False, ENTITY_TYPE: stock_type}
    #     for filter_item in query_params.split('&'):
    #         query_dict[filter_item.split('=')[0]] = filter_item.split('=')[1]
    #
    #     lookup_query = [{'$match': query_dict},
    #                     {'$graphLookup': {'connectToField': '_id', 'connectFromField': 'parent',
    #                                       'from': STOCK_COLLECTION, 'startWith':
    #                                           '$parent', 'as': 'hierarchy'}}]
    #     _count, _records = self.aggregate(STOCK_COLLECTION, lookup_query)
    #     return {'records': marshal(_records, stock_hierarchy_response), 'count': _count}
