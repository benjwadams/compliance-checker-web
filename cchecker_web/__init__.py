#!/usr/bin/env python
'''
Compliance Checker Web
~~~~~~~~~~~~~~~~~~~~~~

'''

from flask import Blueprint, request
from flask import current_app as app

from flask.ext.mail import Mail
from flask.ext.cache import Cache
from flask_wtf.csrf import CsrfProtect
from functools import wraps

# Cache type is specified by config.yml
cache = Cache(config={'CACHE_TYPE':'simple'})
csrf = CsrfProtect()
mail = Mail()


@csrf.error_handler
def csrf_error(reason):
    request.valid_csrf = False

def valid_csrf(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if hasattr(request, 'valid_csrf') and request.valid_csrf is False:
            app.logger.error("Invalid CSRF")
            return jsonify(error='invalid_csrf', message="Invalid CSRF"), 400
        return f(*args, **kwargs)
    return decorated_function


cchecker_web = Blueprint('cchecker_web', __name__, static_url_path='', static_folder='static', template_folder='templates')


from cchecker_web.controller import show_index
from cchecker_web.routes import upload_dataset
from cchecker_web.api import show_job
from cchecker_web.user import show_user
