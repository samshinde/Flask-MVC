#!/usr/bin/env python


class DatabaseOperationFailedError(Exception):
    """
    DatabaseOperationFailedError is a custom exception class used to handle all database failures.
    """

    def __init__(self, error, **kwargs):
        """
        Add custom arguments to an error
        ideally you should use explicit
        inputs for readability

        However in a jam this works nicely
        """
        self.__dict__.update(kwargs)
        Exception.__init__(self, error)

        
class PermissionError(Exception):
    """
    Error for permission denied to a feature
    """

    def __init__(self, message, status_code=403):
        """
           permission error error with specified information.
           :param message: Error message
           :param status_code: Status error code.
           :param headers: Headers for admin errors.
           """
        Exception.__init__(self)
        self.message = message
        self.status_code = status_code

    def to_dict(self):
        rv = dict()
        rv['message'] = self.message
        rv['status_code'] = self.status_code
        return rv


class EntityAlreadyExists(Exception):
    """
    Error for entity already exists
    """

    def __init__(self, entity, message, status_code=409):
        """
           entity exists error with specified information.
           :param message: Error message
           :param status_code: Status error code.
           :param headers: Headers for admin errors.
           """
        Exception.__init__(self)
        self.message = f"{entity} {message}"
        self.status_code = status_code

    def to_dict(self):
        rv = dict()
        rv['message'] = self.message
        rv['status_code'] = self.status_code
        return rv


class EntityNotExists(Exception):
    """
    Error for entity already exists
    """

    def __init__(self, entity, message, status_code=404):
        """
           entity exists error with specified information.
           :param message: Error message
           :param status_code: Status error code.
           :param headers: Headers for admin errors.
           """
        Exception.__init__(self)
        self.message = f"{entity} {message}"
        self.status_code = status_code

    def to_dict(self):
        rv = dict()
        rv['message'] = self.message
        rv['status_code'] = self.status_code
        return rv


class UserOperationError(Exception):
    """
    User Error
    """

    def __init__(self, message, status_code):
        """
           user not activated with specified information.
           :param message: Error message
           :param status_code: Status error code.
           :param headers: Headers for admin errors.
           """
        Exception.__init__(self)
        self.message = message
        self.status_code = status_code

    def to_dict(self):
        rv = dict()
        rv['message'] = self.message
        rv['status_code'] = self.status_code
        return rv
