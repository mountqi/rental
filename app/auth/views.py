import datetime
from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, \
    current_user

from sqlalchemy import and_, or_, not_
from .. import db
from ..models_user import User, UserType, FeeRecord, Fee
from .forms import LoginForm
from . import auth

"""
def is_paid_customer(customer):
    #检查当前中介用户是否在付费允许的时段内

    now = datetime.datetime.now()

    # 下面这个实现不成功，以后再访
    # valid_fee_records = customer.fee_records.\
    #     filter_by(FeeRecord.expire_time>=now).\
    #     filter_by(FeeRecord.start_time<=now).all()
    # return len(valid_fee_records)>0

    # 检查用户所有有效的付费记录
    valid_fee_records = customer.fee_records.filter_by(is_valid=True)\
                        .order_by(FeeRecord.expire_time.desc()).all()
    paid = False
    for record in valid_fee_records:
        if record.start_time<=now and record.expire_time>=now:
            paid = True
            break
    return paid
"""

@auth.route('/auth/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(login_name=form.login_name.data).first()
        if user is not None and user.verify_password(form.password.data):
            if user.user_type is UserType.BACKEND_ADMIN and not user.is_valid():
                flash('账户已经停用')
                return render_template('auth/login.html', form=form)
            elif not user.is_valid():
                flash('亲爱的用户，您尚未付费，或者付费购买的时段已过期。请付费后登录！')
                return render_template('auth/login.html', form=form)

            login_user(user, remember=form.remember_me.data, force=True )
            redirect_url = request.args.get('next')
            if not redirect_url:
                if user.user_type is UserType.BACKEND_ADMIN:
                    redirect_url = url_for('admin.index')
                else:
                    redirect_url = url_for('customer.index')
            return redirect(redirect_url)
        flash('账号或密码不正确')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('您已经退出登录了')
    return redirect(url_for('auth.login'))

