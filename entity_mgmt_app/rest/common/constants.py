#!/usr/bin/env python

SETTINGS_MAP = {
    'development': 'config.DevelopmentConfig',
    'testing': 'config.TestingConfig',
    'staging': 'config.StagingConfig',
    'production': 'config.ProductionConfig',
}

# collections
TASK_COLLECTION = 'tasks'
USER_COLLECTION = 'users'
ENTITY_COLLECTION = 'entities'
ENTITY_TEMPLATE_COLLECTION = 'entity_templates'
ENTITY_TYPE_COLLECTION = 'entity_types'
PRODUCT_TYPE_COLLECTION = 'product_types'
AUTH_LOG_COLLECTION = 'auth_log'
AUDIT_COLLECTION = 'action_audit'
EMAIL_COLLECTION = 'email_alerts'
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
IS_ASSET = 'is_asset'
ENTITY_TYPE = 'entity_type'
ENTITY_TYPE_DETAILS = 'entity_type_details'
PRODUCT_TYPE = 'product_type'
PRODUCT_TYPE_DETAILS = 'product_type_details'
PARENT = 'parent'
PARENT_DETAILS = 'parent_details'
PARENT_TYPE = 'parent_type'
REPORTING_HIERARCHY = 'hierarchy'
LOGIN_TIME = "login_time"
LOGOUT_TIME = 'logout_time'
IS_ACTIVE = "is_active"
FIELDS = 'fields'
STATUS = 'status'
RESERVATION_EXPIRATION = 'reservation_expiration'
RESERVATION_START = 'reservation_start'
RESERVED_UNTIL = 'reserved_until'
RESERVED_FROM = 'reserved_from'
RESERVATION_NOTES = 'reservation_notes'
RESERVATIONS = 'reservations'
ASSIGNED_TO = 'assigned_to'
RESERVED_BY = 'reserved_by'
ASSET_ID = 'asset_id'
MGMT_IP = 'mgmt_ip'
MGMT_IP_ADDRESS = 'mgmt_ip_address'

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