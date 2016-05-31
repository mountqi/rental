import datetime
from flask import render_template, redirect, request, url_for, flash, g
from flask_login import login_user, logout_user, login_required, \
    current_user

from sqlalchemy.exc import IntegrityError
from .. import db
from ..models_user import User, UserType, FeeRecord, Fee, RoleGroup, Agency
from .forms import LoginForm, FindPasswdForm, RegisterPersonalCustomerForm, RegisterCorpCustomerForm, \
    PasswordResetForm
from . import auth
from ..email import send_email
from ..utils import strip

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
        user = User.query.filter_by(login_name=strip(form.login_name.data)).first()
        if user is not None and user.verify_password(strip(form.password.data)):
            if user.user_type is UserType.BACKEND_ADMIN and not user.is_valid():
                flash('账户已经停用')
                return render_template('auth/login.html', form=form)
            elif not user.is_valid():
                flash('亲爱的用户，您尚未付费，或者付费购买的时段已过期。请付费后登录！')
                return render_template('auth/login.html', form=form)

            # login_user(user, remember=form.remember_me.data, force=True )
            login_user(user, remember=False, force=True)
            redirect_url = request.args.get('next')
            if not redirect_url:
                if user.user_type is UserType.BACKEND_ADMIN:
                    redirect_url = url_for('admin.index')
                else:
                    redirect_url = url_for('customer.index')
            return redirect(redirect_url)
        flash('账号或密码不正确')
    g.form = form
    return render_template('auth/login2.html')

@auth.route('/auth/login-old', methods=['GET', 'POST'])
def login_old():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(login_name=strip(form.login_name.data)).first()
        if user is not None and user.verify_password(strip(form.password.data)):
            if user.user_type is UserType.BACKEND_ADMIN and not user.is_valid():
                flash('账户已经停用')
                return render_template('auth/login.html', form=form)
            elif not user.is_valid():
                flash('亲爱的用户，您尚未付费，或者付费购买的时段已过期。请付费后登录！')
                return render_template('auth/login.html', form=form)

            # login_user(user, remember=form.remember_me.data, force=True )
            login_user(user, remember=False, force=True)
            redirect_url = request.args.get('next')
            if not redirect_url:
                if user.user_type is UserType.BACKEND_ADMIN:
                    redirect_url = url_for('admin.index')
                else:
                    redirect_url = url_for('customer.index')
            return redirect(redirect_url)
        flash('账号或密码不正确')

    return render_template('auth/login.html', form=form)


@auth.route('/auth/logout')
@login_required
def logout():
    logout_user()
    # flash('您已经退出登录了')
    return redirect(url_for('auth.login'))

@auth.route('/auth/find-passwd', methods=['GET', 'POST'])
def find_passwd():

    g.form = FindPasswdForm()
    if g.form.validate_on_submit():
        # 在数据库里面搜索，如果不存在这样的地址，则说明出错
        user = User.query.filter_by( email=strip(g.form.email.data) ).first()
        if not user:
            flash('邮箱不正确，请重新填写')
        else:
            # 在这里发送邮件
            if user.user_type == UserType.BACKEND_ADMIN:
                # 管理员不能通过这种方式重置密码
                flash('您不能通过这种方式重置密码，请找管理员解决')
            else:
                g.token = user.generate_reset_token()
                g.user = user
                send_email( strip(g.form.email.data), "重置密码", "mail/reset_passwd", token=g.token )
                return redirect(url_for('auth.passwd_reset_note'))

    g.title_note = "通过两种方式可以找回您的密码"
    g.second_note = "个人用户请携带您注册时用的身份证到我公司重置密码<br/><br/>" + \
                    "公司用户请携带公司营业执照副本到我公司重置密码"

    return render_template('auth/find_passwd.html')


@auth.route('/auth/passwd-reset-note')
def passwd_reset_note():
    g.note = "亲爱的用户，<br/><br/>" + \
        "重置密码的链接已经发到您注册时填写的邮箱，请1分钟后查收邮件。"

    return render_template('auth/passwd_reset_note.html')


@auth.route('/auth/passwd-reset/<token>', methods=['GET', 'POST'])
def passwd_reset(token):
    if not current_user.is_anonymous:
        return redirect(url_for('auth.login'))

    g.form = PasswordResetForm()
    if g.form.validate_on_submit():
        user = User.query.filter_by(email=strip(g.form.email.data)).first()
        if user is None:
            return redirect(url_for('auth.login'))
        if user.reset_password(token, strip(g.form.password.data)):
            flash('密码重置成功')
            return redirect(url_for('auth.login'))
        else:
            flash('密码重置失败了')
            return redirect(url_for('auth.login'))

    return render_template('auth/passwd_reset.html')


@auth.route('/auth/contact-us')
def contact_us():
    g.note = "请用微信扫一扫，添加我们的服务代表"
    return render_template('auth/contact_us.html')


@auth.route('/auth/register-personal', methods=['GET', 'POST'])
def register_personal_customer():
    g.form = RegisterPersonalCustomerForm()
    if g.form.validate_on_submit():
        user = User()
        user.login_name = strip(g.form.login_name.data)
        user.name = strip(g.form.name.data)
        user.password = strip(g.form.password.data)
        user.phone_no = strip(g.form.login_name.data)
        user.email = strip(g.form.email.data)
        role_group = RoleGroup.query.filter_by(name="个人用户组").one()
        user.role_id = role_group.role_id
        user.is_active = False
        user.user_type = UserType.PERSONAL_CUSTOMER
        db.session.add(user)
        try:
            db.session.commit()
            flash('个人用户已经添加')
            print(user.create_time)
            return redirect(url_for('auth.reg_done_note'))
        except IntegrityError as error:
            db.session.rollback()
            flash('用户名已经存在，添加失败', "error")

    return render_template('auth/reg_personal_customer.html')


@auth.route('/auth/register-corp', methods=['GET', 'POST'])
def register_corp_customer():
    g.form = RegisterCorpCustomerForm()

    if g.form.validate_on_submit():
        same_agency1 = Agency.query.filter_by(corp_name=strip(g.form.corp_name.data)).first()
        license_no = strip(g.form.corp_license_no.data)
        same_agency2 = None
        if license_no != "":
            same_agency2 = Agency.query.filter_by(corp_license_no=license_no).first()

        if same_agency1 or same_agency2:
            flash('同名公司已经存在，不能添加', "error")
        else:
            agency = Agency()
            agency.corp_name = strip(g.form.corp_name.data)
            agency.corp_license_no = strip(g.form.corp_license_no.data)
            agency.sub_account_no = 3
            db.session.add(agency)

            user = User()
            user.login_name = strip(g.form.login_name.data)
            user.password = strip(g.form.password.data)
            user.name = strip(g.form.name.data)
            user.phone_no = strip(g.form.login_name.data)
            user.email = strip(g.form.email.data)
            role_group = RoleGroup.query.filter_by(name="公司用户组").one()
            user.role_id = role_group.role_id
            user.is_active = False
            user.user_type = UserType.COPR_CUSTOMER
            user.agency_id = agency.agency_id
            db.session.add(user)
            try:
                db.session.commit()
                return redirect(url_for('auth.reg_done_note'))
            except IntegrityError as error:
                db.session.rollback()
                flash('同名账户已经存在，不能添加', "error")

    return render_template('auth/reg_corp_customer.html')

@auth.route('/auth/reg-done-note')
def reg_done_note():
    g.note = "亲爱的用户，<br/><br/>" + \
        "您的注册已经完成，请耐心等待我们的服务代表审核，审核时间为1个工作日。审核通过后您将收到电子邮件。谢谢您的合作。"

    return render_template('auth/reg_done_note.html')





