from flask import Blueprint

admin = Blueprint('admin', __name__)

from . import views_user,views_customer, views_property
from ..models_user import Permission, role_dict, TimeLengthType
from .. import check_empty

def date_format(date_time):
    return date_time.strftime('%Y-%m-%d')

def datetime_format(date_time):
    return date_time.strftime('%Y-%m-%d %H:%M:%S')

@admin.app_context_processor
def inject_permissions():
    return dict(Permission=Permission,
                check_empty=check_empty,
                role_dict=role_dict,
                len=len,
                date_format=date_format,
                datetime_format=datetime_format,
                TimeLengthType=TimeLengthType )
