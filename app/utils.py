from wtforms import ValidationError
from flask import session

class ServerRequired(object):
    """Form必填字段的验证
    """
    def __init__(self, message=None):
        self.message = message

    def __call__(self, form, field):
        data = str(field.data).strip()
        if len(data) == 0:
            raise ValidationError(self.message)


def strip(data):
    return str(data).strip()


def set_session(key,value):
    session.permanent = True
    session[key] = value