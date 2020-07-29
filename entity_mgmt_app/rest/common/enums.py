#!/usr/bin/env python
from enum import Enum


class ROLES(Enum):
    SUPERADMIN = 1
    ADMIN = 2
    USER = 3


class STATUSES(Enum):
    NEW = 'NEW'
    QUEUED = 'QUEUED'
    IN_PROGRESS = 'IN-PROGRESS'
    PROCESSING = 'PROCESSING'
    COMPLETED = 'COMPLETED'
    FAILED = 'FAILED'


class ENTITY_TYPES(Enum):
    ORGANIZATION = "ORGANIZATION"
    WORKSPACE = "WORKSPACE"
    LOCALITY = "LOCALITY"
    ITEM = "ITEM"
