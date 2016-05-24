from flask import render_template, redirect, request, url_for, flash, g, session

# from flask.ext.login import login_user, logout_user, login_required, \
#     current_user

from flask_login import login_user, logout_user, login_required, \
    current_user

from .. import db
from ..models_user import User, UserType
from ..models_property import District
# from ..email import send_email
from .forms import LoginForm, DateForm, AddEstateForm
from . import experiment

from ..email import send_email, send_async_email



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
from ..utils import set_session

@experiment.route('/experiment/date', methods=['GET','POST'])
def date1():
    form = DateForm()
    # form.start_time.data = date()
    g.hello_today= datetime.now()

    set_session('city',"北京")

    if form.validate_on_submit():
        flash('日期是 {}'.format(form.start_time.data))

    form.start_time.data = date(2011,1,1)
    return render_template('/experiment/date.html',form=form)


@experiment.route('/experiment/two-col-form', methods=['GET','POST'])
def two_col_form():
    form = AddEstateForm( city_id=1 )

    if form.validate_on_submit():
        flash('form are OK')

    return render_template('/experiment/two_col_form.html',form=form)


@experiment.route('/experiment/center-div', methods=['GET'])
def center_div():
    """
    让一个div屏幕居中，好像不起作用！
    """
    return render_template('/experiment/center_div.html')


@experiment.route('/experiment/gui', methods=['GET'])
def gui():
    """
    """
    return render_template('/experiment/gui.html')


@experiment.route('/experiment/login', methods=['GET'])
def login():
    """
    """
    g.form = LoginForm()
    return render_template('/experiment/login1.html')



def rotate_order(order):
    if order == 'no':
        return "up"
    elif order == 'up':
        return "down"
    elif order == 'down':
        return 'up'
    else:
        return 'no'


@experiment.route('/experiment/show-districts', methods=['GET'])
def show_districts():
    """
    """
    g.sort = request.args.get('sort', "districts", type=str)
    g.order = request.args.get('order', "", type=str)
    g.id_order = request.args.get('id_order', "", type=str)

    if g.sort=="districts":
        g.order = rotate_order(g.order)
        g.id_order = "no"
        if g.order == "up":
            g.districts = District.query.order_by(District.district_name).all()
        elif g.order == "down":
            g.districts = District.query.order_by(District.district_name.desc()).all()
        else:
            g.districts = District.query.all()
    else:
        g.id_order = rotate_order(g.id_order)
        g.order = "no"
        if g.id_order == "up":
            g.districts = District.query.order_by(District.district_id).all()
        elif g.id_order == "down":
            g.districts = District.query.order_by(District.district_id.desc()).all()
        else:
            g.districts = District.query.all()


    return render_template('/experiment/show_districts.html')


@experiment.route('/experiment/send-mail', methods=['GET'])
def send_mail():
    """
    """
    return render_template('/experiment/test_mail.html')


@experiment.route('/experiment/send-mail1', methods=['GET'])
def send_mail1():
    """
    """
    to_addr = "mountqi@126.com"
    subject = "test mail sending"
    template = "mail/confirm"
    send_email(to_addr, subject, template)

    return redirect(url_for('experiment.send_mail'))
