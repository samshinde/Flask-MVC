from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple

from auth_app.rest import auth_app
from notification_app.app import mail_app
from entity_mgmt_app.rest import entity_mgmt_app

application = DispatcherMiddleware(
    auth_app, {
        '/entity': entity_mgmt_app,
        '/notification': mail_app
    })

if __name__ == '__main__':
    run_simple(
        hostname='localhost',
        port=5000,
        application=application,
        use_reloader=True,
        use_debugger=True,
        use_evalex=True)
