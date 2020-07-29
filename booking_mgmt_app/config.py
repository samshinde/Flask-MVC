"""
This file holds all of the Flask application configuration
"""
import os
from passlib.hash import sha512_crypt
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    """
    Base Configuration Class Contains all Application Constant Defaults
    """
    SECRET_KEY = os.getenv('SECRET_KEY', 'my_precious_secret_key')
    DEBUG = True

    MONGO_DB_HOST = os.getenv('DB_HOST')
    MONGO_DB_PORT = os.getenv('DB_PORT')
    MONGO_DB_USER = os.getenv('DB_USER')
    MONGO_DB_PASS = os.getenv('DB_PASS')
    MONGO_DB_NAME = os.getenv('DB_NAME')

    APP_ROOT = os.path.dirname(os.path.abspath(__file__))


class ProductionConfig(Config):
    """
    Any Production necessary modifications to Config object Turns off DEBUG
    """
    TESTING = False
    DEBUG = False

    APP_ROOT = os.path.dirname(os.path.abspath(__file__))
    UPLOAD_PATH = APP_ROOT + "/static/"
    TEMPLATES_PATH = APP_ROOT + "/templates"

    # host and port
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = os.getenv('PORT', 5000)
    SCHEMA = os.getenv('SCHEMA', 'http')

    # database configuration
    MONGO_DB_HOST = os.getenv('DB_HOST')
    MONGO_DB_PORT = os.getenv('DB_PORT')
    MONGO_DB_USER = os.getenv('DB_USER')
    MONGO_DB_PASS = os.getenv('DB_PASS')
    MONGO_DB_NAME = os.getenv('DB_NAME')

    # mongo db configuration
    MONGO_URI = 'mongodb://{}:{}@{}:{}/{}'.format(MONGO_DB_USER, MONGO_DB_PASS, MONGO_DB_HOST, MONGO_DB_PORT,
                                                  MONGO_DB_NAME)


class StagingConfig(Config):
    """
    Contains settings and modifications for development environment
    """
    TESTING = False
    DEBUG = False

    APP_ROOT = os.path.dirname(os.path.abspath(__file__))
    UPLOAD_PATH = APP_ROOT + "/static/"
    TEMPLATES_PATH = APP_ROOT + "/templates"

    # host and port
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = os.getenv('PORT', 5003)
    SCHEMA = os.getenv('SCHEMA', 'http')

    # database configuration
    MONGO_DB_HOST = os.getenv('DB_HOST')
    MONGO_DB_PORT = os.getenv('DB_PORT')
    MONGO_DB_USER = os.getenv('DB_USER')
    MONGO_DB_PASS = os.getenv('DB_PASS')
    MONGO_DB_NAME = os.getenv('DB_NAME')

    # mongo db configuration
    MONGO_URI = 'mongodb://{}:{}@{}:{}/{}'.format(MONGO_DB_USER, MONGO_DB_PASS, MONGO_DB_HOST, MONGO_DB_PORT,
                                                  MONGO_DB_NAME)


class TestingConfig(Config):
    """
    Contains settings and modifications for development environment
    """

    TESTING = True
    DEBUG = False

    APP_ROOT = os.path.dirname(os.path.abspath(__file__))
    UPLOAD_PATH = APP_ROOT + "/static/"
    TEMPLATES_PATH = APP_ROOT + "/templates"

    # host and port
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = os.getenv('PORT', 5003)
    SCHEMA = os.getenv('SCHEMA', 'http')

    # database configuration
    MONGO_DB_HOST = os.getenv('DB_HOST', '0.0.0.0')
    MONGO_DB_PORT = os.getenv('DB_PORT', 27017)
    MONGO_DB_USER = os.getenv('DB_USER', 'mongoadmin')
    MONGO_DB_PASS = os.getenv('DB_PASS', 'password')
    MONGO_DB_NAME = os.getenv('DB_NAME', 'booking_mgmt_db')

    # mongo db configuration
    MONGO_URI = 'mongodb://{}:{}@{}:{}/'.format(MONGO_DB_USER, MONGO_DB_PASS, MONGO_DB_HOST, MONGO_DB_PORT)

    REDIS_HOST = os.getenv('REDIS_HOST', '0.0.0.0')

    MAIL_DEFAULT_SENDER = os.getenv('MAIL_USER', "email")
    MAIL_USERNAME = os.getenv('MAIL_USER', "email")
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', "password")
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = "587"
    MAIL_USE_TLS = True

    NOTIFICATION_HOST = os.getenv('NOTIFICATION_HOST', '0.0.0.0')
    NOTIFICATION_PORT = os.getenv('NOTIFICATION_PORT', 5001)

    NOTIFICATION_URL = f"http://{NOTIFICATION_HOST}:{NOTIFICATION_PORT}"

    NOTIFICATION_MAIL_URL = NOTIFICATION_URL + '/api/v1/mail/'

    ERROR_404_HELP = False


class DevelopmentConfig(Config):
    """
    Contains settings and modifications for development environment.
    This is the configuration to use with Docker
    """
    TESTING = False
    DEBUG = True

    APP_ROOT = os.path.dirname(os.path.abspath(__file__))
    UPLOAD_PATH = APP_ROOT + "/static/"
    TEMPLATES_PATH = APP_ROOT + "/templates"

    # host and port
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = os.getenv('PORT', 5003)
    SCHEMA = os.getenv('SCHEMA', 'http')

    # database configuration
    MONGO_DB_HOST = os.getenv('DB_HOST', '0.0.0.0')
    MONGO_DB_PORT = os.getenv('DB_PORT', 27017)
    MONGO_DB_USER = os.getenv('DB_USER', 'mongoadmin')
    MONGO_DB_PASS = os.getenv('DB_PASS', 'password')
    MONGO_DB_NAME = os.getenv('DB_NAME', 'booking_mgmt_db')

    # mongo db configuration
    MONGO_URI = 'mongodb://{}:{}@{}:{}/'.format(MONGO_DB_USER, MONGO_DB_PASS, MONGO_DB_HOST, MONGO_DB_PORT)

    REDIS_HOST = os.getenv('REDIS_HOST', '0.0.0.0')

    MAIL_DEFAULT_SENDER = os.getenv('MAIL_USER', "email")
    MAIL_USERNAME = os.getenv('MAIL_USER', "email")
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', "password")
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = "587"
    MAIL_USE_TLS = True

    NOTIFICATION_HOST = os.getenv('NOTIFICATION_HOST', '0.0.0.0')
    NOTIFICATION_PORT = os.getenv('NOTIFICATION_PORT', 5001)

    NOTIFICATION_URL = f"http://{NOTIFICATION_HOST}:{NOTIFICATION_PORT}"

    NOTIFICATION_MAIL_URL = NOTIFICATION_URL + '/api/v1/mail/'

    ERROR_404_HELP = False
