#!/usr/bin/env python3
from rest import entity_mgmt_app as application
from rest import manager as app_manager
from rest import api

# views
from rest.health_check.views import health_check_api_ns
from rest.entities.views import entity_api_ns
from rest.entities.templates.views import entity_template_api_ns
from rest.entity_types.views import entity_type_api_ns

BASE_API = "/api/v1/entity"

api.add_namespace(entity_api_ns, path=f'{BASE_API}')
api.add_namespace(health_check_api_ns, path=f'{BASE_API}/status')
api.add_namespace(entity_template_api_ns, path=f'{BASE_API}/template')
api.add_namespace(entity_type_api_ns, path=f'{BASE_API}/type')

# init app
api.init_app(application)


@app_manager.command
def seed():
    """
    seed data into database
    :return:
    """
    print("sample seed commands")



if __name__ == '__main__':
    application.run(threaded=True, host=application.config['HOST'], port=application.config['PORT'],
                    debug=application.config['DEBUG'])
