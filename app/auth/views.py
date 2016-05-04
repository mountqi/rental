from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, \
    current_user

from .. import db
from ..user_models import User, UserType
from .forms import LoginForm
from . import auth


@auth.route('/auth/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(login_name=form.login_name.data).first()
        if user is not None and user.verify_password(form.password.data):
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

