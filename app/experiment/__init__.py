from flask import Blueprint
from flask_nav import Nav
from flask_nav.elements import Navbar, View, Subgroup, Link, Separator


experiment = Blueprint('experiment', __name__)

from . import views

