from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, \
    current_user

from . import customer
from .. import db

@customer.route('/customer')
@login_required
def index():
    return "<h1>logged in to customer</h1>"


