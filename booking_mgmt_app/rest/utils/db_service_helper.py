"""
Service helper
"""


def get_limit_skip(**kwargs):
    """
    function to calculate limit and skip
    :param kwargs:
    :return: limit, skip
    """
    size = kwargs.get("size")
    page = kwargs.get("page")
    limit = kwargs.get("limit")
    skip = kwargs.get("skip")
    if size or page is not None:
        if page == 1:
            limit = size
            skip = 0
        else:
            page = (page - 1) * size
            limit = size
            skip = page
    return limit, skip


def get_document_order_by(self, collection_name, filter_dictionary, **kwargs):
    """
    function to get documents based on orderby and sortby
    :param self:
    :param collection_name:
    :param filter_dictionary:
    :param kwargs:
    :return:
    """
    projection = kwargs.get("projection", {})
    if projection:
        if kwargs.get("order_by") == 'desc':
            cursor = self.client[collection_name].find(filter_dictionary, projection). \
                sort([(kwargs.get("sort_by"), -1)]). \
                skip(kwargs.get("skip")).limit(kwargs.get("limit"))
        else:
            cursor = self.client[collection_name].find(filter_dictionary, projection). \
                sort([(kwargs.get("sort_by"), 1)]).skip(kwargs.get("skip")). \
                limit(kwargs.get("limit"))
    else:
        if kwargs.get("order_by") == 'desc':
            cursor = self.client[collection_name].find(filter_dictionary). \
                sort([(kwargs.get("sort_by"), -1)]).skip(kwargs.get("skip")). \
                limit(kwargs.get("limit"))
        else:
            cursor = self.client[collection_name].find(filter_dictionary). \
                sort([(kwargs.get("sort_by"), 1)]). \
                skip(kwargs.get("skip")).limit(kwargs.get("limit"))
    return cursor


def get_document_limit(self, collection_name, filter_dictionary, **kwargs):
    """

    :param self:
    :param collection_name:
    :param filter_dictionary:
    :param kwargs:
    :return:
    """
    projection = kwargs.get("projection", {})
    if projection:
        cursor = self.client[collection_name].find(filter_dictionary, projection) \
            .skip(kwargs.get("skip")).limit(kwargs.get("limit"))
    else:
        cursor = self.client[collection_name].find(filter_dictionary) \
            .skip(kwargs.get("skip")).limit(kwargs.get("limit"))
    return cursor


def get_document(self, collection_name, filter_dictionary, **kwargs):
    """

    :param self:
    :param collection_name:
    :param filter_dictionary:
    :param kwargs:
    :return:
    """
    projection = kwargs.get("projection", {})
    if projection:
        cursor = self.client[collection_name].find(filter_dictionary, projection)
    else:
        cursor = self.client[collection_name].find(filter_dictionary)
    return cursor
