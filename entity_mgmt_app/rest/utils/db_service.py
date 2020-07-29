"""
Base mongo db reports
"""

import logging
from sys import maxsize

from pymongo.errors import ConnectionFailure
from rest import mongo_db
from rest.common.errors import DatabaseOperationFailedError
from rest.common import messages
from rest.utils.db_service_helper import get_limit_skip, get_document_order_by, \
    get_document_limit, get_document


class Base(object):
    """
    Abstract db activities by this class
    """

    def __init__(self):
        self.client = mongo_db

    def create(self, collection_name, records):
        """
        Add a new 'record(s)' to 'collection'.
        This function should handle both single and multiple record creation.
        :param collection_name:
        :param records:
        :return: Single or Multiple IDs based on inputs
        """
        try:
            logging.info("Creating the collection in db.")
            collection = self.client[collection_name]
            is_list = isinstance(records, list)
            if is_list:  # array, use insert_many
                logging.info("Performing insert many operation.")
                result = collection.insert_many(records)
                return True, result.inserted_ids
            logging.info("Performing insert one operation")
            result = collection.insert_one(records)
            return True, result.inserted_id
        except BaseException as ex:
            logging.exception(ex)
            logging.error("Error while performing insert reports.")
            raise DatabaseOperationFailedError(ex)

    def get(self, collection_name, filter_dictionary={}, **kwargs):
        """
        Find many or Find one record
        :param filter_dictionary:
        :param collection_name:
        :return: count, list of records
        """

        try:
            is_dictionary = isinstance(filter_dictionary, dict)
            if not is_dictionary:
                logging.warning("DB Get operation: filter_dict is not a instance of dict")
                raise TypeError(messages.INVALID_TYPE_DEFAULT)

            limit, skip = get_limit_skip(**kwargs)
            if kwargs.get("sort_by") and kwargs.get("order_by"):
                if not skip and not limit:
                    skip = 0
                    limit = maxsize
                cursor = get_document_order_by(self, collection_name, filter_dictionary,
                                               limit=limit, skip=skip, **kwargs)
            elif limit:
                cursor = get_document_limit(self, collection_name, filter_dictionary,
                                            limit=limit, skip=skip, **kwargs)
            else:
                cursor = get_document(self, collection_name, filter_dictionary, **kwargs)

            count = cursor.count()
            records = list(cursor)

            logging.info("DB GET operation: count %s of records. ", count)

            return count, records
        except BaseException as ex:
            logging.error("Error while performing db get operation")
            logging.exception(ex)
            raise DatabaseOperationFailedError(ex)

    def update(self, collection_name, **kwargs):
        """
        update the document or documents
        :param collection_name:
        :param kwargs:
        :return:
        """
        multi = kwargs.get("multi", False)
        query = kwargs.get("query", {})
        upsert = kwargs.get("upsert", False)
        updated_record = kwargs.get("updated_record", {})
        updated_query = kwargs.get("update_query", {})
        try:
            if updated_query:
                cursor = self.client[collection_name]. \
                    update(query, updated_query)

            elif multi:
                cursor = self.client[collection_name]. \
                    update_many(query, {'$set': updated_record}, upsert)
            else:
                cursor = self.client[collection_name]. \
                    update_one(query, {'$set': updated_record}, upsert)

            return cursor

        except (BaseException, ConnectionFailure) as ex:
            logging.error(ex)
            logging.error('Failed to perform update operation for %s', collection_name)
            raise DatabaseOperationFailedError(ex)

    def get_total_count(self, collection_name, filter_dictionary):
        """
        funtion to get total records count for resource API
        :param collection_name:
        :param filter_dictionary:
        :return:
        """
        try:
            total_count = self.client[collection_name].find(filter_dictionary).count()
            return total_count

        except (BaseException, ConnectionFailure) as ex:
            logging.error(ex)
            logging.error('Failed to perform update operation for %s', collection_name)
            raise DatabaseOperationFailedError(ex)

    def aggregate(self, collection_name, query):
        """
        aggregation query
        :param collection_name:
        :param query:
        :return:
        """
        try:
            cursor = self.client[collection_name].aggregate(query)
            records = list(cursor)
            count = len(records)
            return count, records
        except (BaseException, ConnectionFailure) as ex:
            logging.error(ex)
            logging.error('Failed to perform update operation for %s', collection_name)
            raise DatabaseOperationFailedError(ex)

    def delete(self, collection_name, query):
        """
        Delete Records
        :param collection_name:
        :param query:
        :return:
        """
        try:
            cursor = self.client[collection_name].remove(query)
            return cursor
        except (BaseException, ConnectionFailure) as ex:
            logging.error(ex)
            logging.error('Failed to perform delete operation for %s', collection_name)
            raise DatabaseOperationFailedError(ex)
