from flask import Blueprint

customer = Blueprint('customer', __name__)
from . import views

# from . import views, errors
# from ..models import Permission


# @main.app_context_processor
# def inject_permissions():
#     return dict(Permission=Permission)
