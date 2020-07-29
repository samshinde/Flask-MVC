from bson import ObjectId
from flask_restplus import abort, marshal

from rest.booking.models import booking_response
from rest.common.constants import BOOKING_COLLECTION, NAME, ID, PARENT_DETAILS, PARENT_TYPE
from rest.common.constants import META, IS_DELETED, ENTITY_TYPE, ENTITY_TYPE_DETAILS, PARENT, UPDATED, \
    INTERNAL_SERVER_ERROR, \
    ENTITY_NOT_FOUND, ENTITY_ALREADY_EXISTS
from rest.utils.dateutils import get_current_time
from rest.utils.db_service import Base


class BookingService(Base):
    def create_booking(self, req_data, booking_type_obj):
        """
        create entities
        :param req_data:
        :param booking_type_obj:
        :return:
        """
        _count, _booking = self.get(BOOKING_COLLECTION,
                                   {f"{META}.{IS_DELETED}": False,
                                   NAME: req_data[NAME],
                                   ENTITY_TYPE: booking_type_obj.get('name')})

        if _count == 1 and _booking:
            abort(ENTITY_ALREADY_EXISTS, message="Entity already exists with given name.", status=ENTITY_ALREADY_EXISTS)

        req_data[ENTITY_TYPE] = booking_type_obj.get('name')
        req_data[ENTITY_TYPE_DETAILS] = booking_type_obj

        if req_data.get(PARENT):
            req_data[PARENT] = ObjectId(req_data.get(PARENT))

        result, _id = self.create(BOOKING_COLLECTION, req_data)

        if result:
            req_data[ID] = _id
            return marshal(req_data, booking_response)
        else:
            abort(INTERNAL_SERVER_ERROR, message='Error in inserting records to {} collection'.format(BOOKING_COLLECTION),
                  status=INTERNAL_SERVER_ERROR)

    def get_bookings_by_type(self, booking_type, search_dict=None, page=1, size=1000, sort_by="name", order_by="asc"):
        """
        get all entities
        :param booking_type:
        :param search_dict:
        :param page:
        :param size:
        :param sort_by:
        :param order_by:
        :return: list entities by booking type
        """
        query_dict = {f"{META}.{IS_DELETED}": False,
                 ENTITY_TYPE: booking_type}

        if search_dict is not None:
            query_dict.update(search_dict)

        _count, _bookings = self.get(BOOKING_COLLECTION,
                                    query_dict,
                                    sort_by=sort_by,
                                    order_by=order_by,
                                    page=page,
                                    size=size)
        return {'records': marshal(_bookings, booking_response), 'count': _count}

    def filter_bookings(self, query_params, booking_type, search_dict=None, page=1, size=1000, sort_by="name", order_by="asc"):
        """
        apply query params to aggregate query
        :param query_params:
        :param booking_type:
        :param search_dict:
        :param page:
        :param size:
        :param sort_by:
        :param order_by:
        :return:
        """
        query_dict = {f'{META}.{IS_DELETED}': False,
                      ENTITY_TYPE: booking_type}

        if search_dict is not None:
            query_dict.update(search_dict)

        if isinstance(query_params, str) and "&" in query_params:
            for filter_item in query_params.split('&'):
                query_dict[filter_item.split('=')[0]] = filter_item.split('=')[1]
        elif isinstance(query_params, dict):
            query_dict.update(query_params)

        _count, _bookings = self.get(BOOKING_COLLECTION,
                                    query_dict,
                                    sort_by=sort_by,
                                    order_by=order_by,
                                    page=page,
                                    size=size)
        return {'records': marshal(_bookings, booking_response), 'count': _count}

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

    def get_bookings_by_name(self, booking_name, booking_type=None, raise_error=True):
        """
        get booking
        :param booking_name
        :param booking_type
        :param raise_error
        :return: get booking by name
        """
        if booking_type:
            _count, _booking = self.get(BOOKING_COLLECTION, {f"{META}.{IS_DELETED}": False,
                                                         "name": booking_name,
                                                            ENTITY_TYPE:booking_type})
        else:
            _count, _booking = self.get(BOOKING_COLLECTION, {f"{META}.{IS_DELETED}": False,
                                                         "name": booking_name})
        if _count == 1 and _booking:
            return marshal(_booking[0], booking_response)
        elif raise_error:
            abort(ENTITY_NOT_FOUND, message="Entity with name {} does not exists.".format(booking_name),
                  status=ENTITY_NOT_FOUND)
        else:
            return None

    def get_booking(self, booking_type, booking_id, raise_error=True):
        """
        get entities by _id
        :param booking_type
        :param booking_id:
        :return:
        """
        _count, _booking = self.get(BOOKING_COLLECTION, {f"{META}.{IS_DELETED}": False,
                                                        ID: ObjectId(booking_id),
                                                        ENTITY_TYPE: booking_type})
        if _count == 1 and _booking:
            return marshal(_booking[0], booking_response)
        elif raise_error:
            abort(ENTITY_NOT_FOUND, message="booking {} with {} does not exists.".format(booking_type, booking_id),
                  status=ENTITY_NOT_FOUND)
        else:
            return None

    def get_booking_by_id(self, booking_id, raise_error=True):
        """
        get entities by _id
        :param booking_type
        :param booking_id:
        :return:
        """
        _count, _booking = self.get(BOOKING_COLLECTION, {f"{META}.{IS_DELETED}": False,
                                                        ID: ObjectId(booking_id)})
        if _count == 1 and _booking:
            return marshal(_booking[0], booking_response)
        elif raise_error:
            abort(ENTITY_NOT_FOUND, message="Entity with ID : {} does not exists.".format(booking_id),
                  status=ENTITY_NOT_FOUND)
        else:
            return None

    def update_booking(self, req_data, booking_type, booking_id):
        """
        update entities
        :param req_data:
        :param booking_type
        :param booking_id:
        :return:
        """
        _booking = self.get_booking(booking_type, booking_id)
        if _booking:
            req_data[META] = _booking[META]
            req_data[META][UPDATED] = get_current_time()

            if req_data.get(PARENT):
                parent = self.get_booking(req_data.get(PARENT_TYPE), req_data.get(PARENT))
                req_data[PARENT_DETAILS] = parent

            self.update(BOOKING_COLLECTION,
                        query={f"{META}.{IS_DELETED}": False, ID: ObjectId(booking_id)},
                        updated_record=req_data)

            _booking = self.get_booking(booking_type, booking_id)
            self.update(BOOKING_COLLECTION,
                        query={f"{META}.{IS_DELETED}": False,
                               f"{PARENT_DETAILS}.{ID}": booking_id},
                        updated_record={PARENT_DETAILS: _booking},
                        multi=True)
        else:
            abort(ENTITY_NOT_FOUND,
                  message="Entity {} with id {} doesn't exists to update".format(booking_type, booking_id),
                  status=ENTITY_NOT_FOUND)

        return _booking

    def delete_booking(self, booking_id):
        """
        delete entities by _id
        :param booking_id:
        :return:
        """
        self.update(BOOKING_COLLECTION, query={ID: ObjectId(booking_id)},
                    update_query={"$set": {f"{META}.{IS_DELETED}": True}})

    # def list_bookings_hierarchy(self):
    #     lookup_query = [{'$match': {f'{META}.{IS_DELETED}': False}},
    #                     {'$graphLookup': {'connectToField': '_id', 'connectFromField': 'parent',
    #                                       'from': BOOKING_COLLECTION, 'startWith':
    #                                           '$parent', 'as': 'hierarchy'}}]
    #     _count, _records = self.aggregate(BOOKING_COLLECTION, lookup_query)
    #     return {'records': marshal(_records, booking_hierarchy_response), 'count': _count}
    #
    # def list_bookings_hierarchy_by_type(self, booking_type):
    #     """
    #     list entities hierarchy by type
    #     :param booking_type:
    #     :return:
    #     """
    #     lookup_query = [{'$match': {f"{META}.{IS_DELETED}": False, ENTITY_TYPE: booking_type}},
    #                     {'$graphLookup': {'connectToField': '_id', 'connectFromField': 'parent',
    #                                       'from': BOOKING_COLLECTION, 'startWith': '$parent', 'as': 'hierarchy'}}]
    #
    #     _count, _bookings = self.aggregate(BOOKING_COLLECTION, lookup_query)
    #     return {'records': marshal(_bookings, booking_hierarchy_response), 'count': _count}
    #
    # def filter_bookings_hierarchy(self, query_params, booking_type):
    #     """
    #     apply query params to aggregate query
    #     :param query_params:
    #     :return:
    #     """
    #     query_dict = {f'{META}.{IS_DELETED}': False, ENTITY_TYPE: booking_type}
    #     for filter_item in query_params.split('&'):
    #         query_dict[filter_item.split('=')[0]] = filter_item.split('=')[1]
    #
    #     lookup_query = [{'$match': query_dict},
    #                     {'$graphLookup': {'connectToField': '_id', 'connectFromField': 'parent',
    #                                       'from': BOOKING_COLLECTION, 'startWith':
    #                                           '$parent', 'as': 'hierarchy'}}]
    #     _count, _records = self.aggregate(BOOKING_COLLECTION, lookup_query)
    #     return {'records': marshal(_records, booking_hierarchy_response), 'count': _count}
