#!/usr/bin/env python
"""
This is a utility class used as factory to perform repetitive reports
across project to avoid code duplication.
"""

import random
import string

import jinja2
import requests
from flask_mail import Message
from flask_restplus import marshal
from jinja2 import Environment, FileSystemLoader

from rest import entity_mgmt_app, logger
from rest.utils.dateutils import get_current_time, reformat


def get_application_url():
    return f"{entity_mgmt_app.config.get('SCHEMA')}://{entity_mgmt_app.config.get('HOST')}:{entity_mgmt_app.config.get('PORT')}"


def custom_marshal(data, model, **kwargs):
    result = marshal(data, model, **kwargs)
    if "meta" in result:
        result['meta']['created'] = get_current_time().isoformat()
        result['meta']['updated'] = get_current_time().isoformat()
    return result


def get_dynamic_dir_name(backup_name):
    return f"{backup_name}-{reformat(get_current_time(),'%d-%m-%Y-%H:%M:%S')}"
