from functools import wraps
from flask import abort
#from flask.ext.login import current_user
from flask_login import current_user
from .models_user import Permission

def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.can(permission):
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator

