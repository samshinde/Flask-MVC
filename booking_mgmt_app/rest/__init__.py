#!/usr/bin/env python
import json
import os
import logging
from datetime import timedelta
from logging.handlers import RotatingFileHandler

import jwt
from flask import Flask, g, request
from flask_jwt_extended.exceptions import RevokedTokenError, NoAuthorizationError
from flask_restplus import Api
# from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from pymongo import MongoClient
import redis
from flask_jwt_extended import JWTManager, get_jwt_claims

from rest.common.constants import SETTINGS_MAP
from rest.common.errors import PermissionError, EntityAlreadyExists, EntityNotExists, UserOperationError


def set_logger(app):
    """
    Set global logger
    :return:
    """
    # Logger configuration
    log_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), os.pardir) + os.path.sep + 'log'
    if not os.path.exists(log_path):
        os.makedirs(log_path)

    formatter = logging.Formatter(
        "[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s")

    handler = RotatingFileHandler(log_path + os.path.sep + 'app.log', maxBytes=10000000, backupCount=1)
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)
    app.logger.debug("Logger Initiated")
    return app.logger


# Create app object which is for itsm app to a runtime environment
entity_mgmt_app = Flask(__name__, template_folder='../templates')
entity_mgmt_app.config.from_object(SETTINGS_MAP[os.getenv('FLASK_CONFIGURATION', 'development')])

# mongo connection instance
conn = MongoClient(entity_mgmt_app.config['MONGO_URI'])
mongo_db = conn[entity_mgmt_app.config['MONGO_DB_NAME']]

# redis connection instance
redis_conn = redis.StrictRedis(host=entity_mgmt_app.config['REDIS_HOST'], port=6379, db=0,
                               decode_responses=True)

# Api settings
api = Api(version='1.0',
          title='Anyserve Forum API',
          doc='/api/v1',
          description='REST API OF Entity Management FORUM BACKEND',
          contact='samshinde23290@gmail.com',
          default='status')

# Set current user
with entity_mgmt_app.app_context():
    current_user = None
    g.current_user = current_user

# logger
logger = set_logger(entity_mgmt_app)

manager = Manager(entity_mgmt_app)
# migrate = Migrate(app, db)
# manager.add_command('db', MigrateCommand)


# jwt manager init
ACCESS_EXPIRES = timedelta(hours=24)
REFRESH_EXPIRES = timedelta(days=30)
entity_mgmt_app.config['JWT_ACCESS_TOKEN_EXPIRES'] = ACCESS_EXPIRES
entity_mgmt_app.config['JWT_REFRESH_TOKEN_EXPIRES'] = REFRESH_EXPIRES
entity_mgmt_app.config['JWT_SECRET_KEY'] = entity_mgmt_app.config.get('SECRET_KEY')
entity_mgmt_app.config['JWT_BLACKLIST_ENABLED'] = True
entity_mgmt_app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
jwt_flask = JWTManager(entity_mgmt_app)


@jwt_flask.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    key = f"{decrypted_token['identity']['_id']}_{decrypted_token['type']}"
    entry = redis_conn.get(key)
    if entry is None or entry == 'None':
        return True


@api.errorhandler(Exception)
def handle_error(e):
    if isinstance(e, jwt.DecodeError):
        code = 401
        message = "Invalid token"
    elif isinstance(e, jwt.ExpiredSignatureError):
        code = 401
        message = "Token has expired"
    elif isinstance(e, PermissionError):
        code = e.status_code
        message = e.message
    elif isinstance(e, EntityAlreadyExists):
        code = e.status_code
        message = e.message
    elif isinstance(e, EntityNotExists):
        code = e.status_code
        message = e.message
    elif isinstance(e, UserOperationError):
        code = e.status_code
        message = e.message
    elif isinstance(e, RevokedTokenError):
        code = 401
        message = "Token has expired"
    elif isinstance(e, NoAuthorizationError):
        code = 400
        message = "Missing Authorization Header"
    else:
        code = 500
        message = e.__str__()
    return {"status": code, "message": message}, code


# parser
auth_header_parser = api.parser()
auth_header_parser.add_argument('Authorization', location='headers')

from rest.audit.models import audit as audit_model
from rest.utils.db_service import Base
from rest.common.constants import AUDIT_EVENT
from rest.common.utils import custom_marshal

db = Base()


@entity_mgmt_app.after_request
def audit(response):
    _request = request.__dict__
    if _request['environ']['REQUEST_METHOD'] in ['POST', 'PUT', 'DELETE'] and \
            '/api/v1/metrics' not in _request['environ']['PATH_INFO']:
        req_data = {}
        if request.data:
            req_data = json.loads(request.data)

        _response = json.loads(response.data.decode())

        if _response and _response.get('status') in [200, 201]:
            result = "SUCCESS"
        else:
            result = "FAIL"

        claims = get_jwt_claims()
        email = claims.get('email') if claims else req_data.get('email', '')

        audit_data = {
            'method': _request['environ']['REQUEST_METHOD'],
            'req_data': req_data,
            'event': _request['url_rule'].endpoint,
            'endpoint': _request['environ']['PATH_INFO'],
            'query_param': _request['view_args'],
            'result': result,
            'message': _response.get('message', ''),
            'status': _response.get('status', 500),
            'meta': {
                'created_by': email
            }
        }
        db.create(AUDIT_EVENT, custom_marshal(audit_data, audit_model))
    return response
