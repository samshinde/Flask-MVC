#!/usr/bin/env python

SETTINGS_MAP = {
    'development': 'config.DevelopmentConfig',
    'testing': 'config.TestingConfig',
    'staging': 'config.StagingConfig',
    'production': 'config.ProductionConfig',
}

# collections
TASK_COLLECTION = 'tasks'
ENTITY_COLLECTION = 'entities'
ENTITY_TEMPLATE_COLLECTION = 'entity_templates'
ENTITY_TYPE_COLLECTION = 'entity_types'
AUDIT_COLLECTION = 'action_audit'
AUDIT_EVENT = 'audit_event'
APPLICATION_STATUS_COLLECTION = 'application_status'

# fields
ID = '_id'
QUERY = 'query'
UPDATED_RECORD = 'updated_record'
RECORD = 'record'
EMAIL = 'email'
PASSWORD = 'password'
ROLE_COLLECTION = 'role'
META = 'meta'
IS_DELETED = 'is_deleted'
CREATED = 'created'
UPDATED = 'updated'
CREATED_BY = 'created_by'
UPDATED_BY = 'updated_by'
NAME = 'name'
IS_ACTIVE = "is_active"
FIELDS = 'fields'
STATUS = 'status'

# status codes
SUCCESS = 200
BAD_REQUEST = 400
ENTITY_NOT_FOUND = 404
ENTITY_ALREADY_EXISTS = 409
HTTP_401_UNAUTHORIZED = 401
INTERNAL_SERVER_ERROR = 500
FORBIDDEN = 403
UNAUTHORIZED = 401
CREATED_STATUS = 201
MAINTENANCE = 503

# other
ROLE_NAME = 'role_name'
EVENT = 'event'
RETRY = 3