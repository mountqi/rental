from flask import render_template, redirect, request, url_for, flash

# from flask.ext.login import login_user, logout_user, login_required, \
#     current_user

from flask_login import login_user, logout_user, login_required, \
    current_user

from .. import db
from ..user_models import User, UserType
# from ..email import send_email
from .forms import LoginForm, DateForm
from . import experiment

tab_menu = [
    ("个人用户","admin.personal_customers",False),
    ("公司用户", "admin.corp_customers", True),
    ("缴费退费", "admin.fee_standards", False),
    ("收费标准", "admin.fee_standards", False),
]

nav_menu = {
    "title":"后台导航",
    "menu" :
        [
        ("个人用户","admin.personal_customers","menu"),
        ("公司用户", "admin.corp_customers", "menu"),
        ("", "", "sep"),
        ("收费标准", "admin.fee_standards", "menu"),
        ]
}

@experiment.route('/experiment/base', methods=['GET'])
def base():
    return render_template('/experiment/base2.html',\
                           tab_menu=tab_menu,\
                           nav_menu=nav_menu,\
                           title="公司用户 -- 添加新用户")



from datetime import datetime, date

@experiment.route('/experiment/date', methods=['GET','POST'])
def date1():
    form = DateForm()
    # form.start_time.data = date()

    if form.validate_on_submit():
        flash('日期是 {}'.format(form.start_time.data))

    form.start_time.data = date(2011,1,1)
    return render_template('/experiment/date.html',form=form)


