"""
前端个人用户
前端公司用户
收费
"""
import datetime
from dateutil.relativedelta import relativedelta
from sqlalchemy.exc import IntegrityError
from sqlalchemy import and_, or_, not_
from flask import render_template, redirect, request, url_for, flash, jsonify
from flask_login import login_required, current_user

from . import admin
from .forms import AddPersonalUserForm, ModifyPersonalUserForm,ChangeUserPasswordForm, \
    AddCorpCustomerForm, ModifyCorpCustomerForm, AddFeeStandardForm, ChargeFeeForm

from .. import db, check_empty
from ..user_models import User, UserType, Agency, Fee, FeeRecord, RoleGroup, TimeLengthType
from .menu_factory import get_nav_menu, get_tab_menu


@admin.route('/admin/personal-customers',methods=['GET'])
@login_required
def personal_customers():
    """浏览个人用户
    """
    page = request.args.get('page', 1, type=int)
    pagination = User.query.filter_by(user_type=UserType.PERSONAL_CUSTOMER).paginate(
        page, per_page=10, error_out=False)
    customers = pagination.items
    return render_template('admin/personal_customers.html',
                           customers=customers, pagination=pagination,
                           title="查看个人用户", nav_menu=get_nav_menu(current_user),
                           tab_menu=get_tab_menu("customers", current_user, "个人用户"))


@admin.route('/admin/add-personal-user',methods=['GET', 'POST'])
@login_required
def add_personal_user():
    """添加个人用户
    """
    form = AddPersonalUserForm()
    if form.validate_on_submit():
        user = User()
        user.login_name = form.login_name.data
        user.name = form.name.data
        user.password = str(form.password.data).strip()
        user.phone_no = form.phone_no.data
        user.email = form.email.data
        user.remark = form.remark.data
        role_group = RoleGroup.query.filter_by(name="个人用户组").one()
        user.role_id = role_group.role_id
        user.is_active = False
        user.user_type = UserType.PERSONAL_CUSTOMER
        db.session.add(user)
        try:
            db.session.commit()
            flash('个人用户已经添加')
            print(user.create_time)
            return redirect(url_for('admin.personal_customers'))
        except IntegrityError as error:
            db.session.rollback()
            flash('用户名已经存在，添加失败', "error")

    return render_template("admin/common.html", form=form,
                           title="添加个人用户", nav_menu=get_nav_menu(current_user),
                           tab_menu=get_tab_menu("customers", current_user, "个人用户"))


@admin.route('/admin/mod-personal-user/<user_id>',methods=['GET', 'POST'])
@login_required
def mod_personal_user(user_id):
    """查看和修改个人用户信息
    """
    form = ModifyPersonalUserForm()
    user = User.query.filter_by(user_id=user_id).one()
    if form.validate_on_submit():
        user.login_name = form.login_name.data
        user.name = form.name.data
        user.phone_no = form.phone_no.data
        user.email = form.email.data
        user.remark = form.remark.data
        # ??? active 状态应该是根据缴费来定的
        # user.is_active = form.status.data
        db.session.add(user)
        db.session.commit()
        flash('用户信息已经更新')
        return redirect( url_for('admin.personal_customers') )

    form.login_name.data = user.login_name
    form.name.data = check_empty(user.name)
    form.phone_no.data = check_empty(user.phone_no)
    form.email.data = check_empty(user.email)
    form.remark.data = check_empty(user.remark)
    return render_template("admin/mod_personal_user.html", form=form, user_id=user_id,
                           title="查看和修改个人用户资料", nav_menu=get_nav_menu(current_user),
                           tab_menu=get_tab_menu("customers", current_user, "个人用户"))


@admin.route('/admin/new-passwd/<int:user_id>',methods=['GET', 'POST'])
@login_required
def new_passwd(user_id):
    """为个人用户和公司用户设定新密码
    """
    form = ChangeUserPasswordForm()
    user = User.query.filter_by(user_id=user_id).one()
    if form.validate_on_submit():
        user.password = form.password.data
        db.session.add(user)
        flash('用户的密码已经更新')
        return redirect(request.args.get('next') or url_for('admin.personal_customers'))
    next = request.args.get('next')
    action = url_for('admin.new_passwd',user_id=user_id,next=next)
    return render_template("admin/new_passwd.html", form=form, action=action,
                           title="为用户设定新密码", nav_menu=get_nav_menu(current_user),
                           tab_menu=None)


@admin.route('/admin/corp-customers',methods=['GET'])
@login_required
def corp_customers():
    """查看公司用户列表
    """
    page = request.args.get('page', 1, type=int)
    pagination = User.query.filter_by(user_type=UserType.COPR_CUSTOMER).paginate(
        page, per_page=10, error_out=False)
    customers = pagination.items
    return render_template('admin/corp_customers.html',
                           customers=customers, pagination=pagination,
                           title="查看公司用户", nav_menu=get_nav_menu(current_user),
                           tab_menu=get_tab_menu("customers", current_user, "公司用户"))


@admin.route('/admin/add-corp-customer',methods=['GET', 'POST'])
@login_required
def add_corp_customer():
    """添加公司用户
    """
    form = AddCorpCustomerForm()
    if form.validate_on_submit():

        # same_agency = db.session.query(Agency).filter( or_(Agency.corp_name==form.corp_name.data,
        #                                                    Agency.corp_license_no==form.corp_license_no.data) ).first()
        same_agency1 = Agency.query.filter_by(corp_name = form.corp_name.data).first()
        license_no = str(form.corp_license_no.data).strip()
        same_agency2 = None
        if license_no != "":
            same_agency2 = Agency.query.filter_by(corp_license_no = license_no).first()

        if same_agency1 or same_agency2:
            flash('同名公司已经存在，不能添加', "error")
        else:
            agency = Agency()
            agency.corp_name = form.corp_name.data
            agency.corp_license_no = form.corp_license_no.data
            # agency.is_active = False
            agency.sub_account_no = form.sub_account_no.data
            db.session.add(agency)

            user = User()
            user.login_name = form.login_name.data
            user.password = str(form.password.data).strip()
            user.name = form.name.data
            # user.id_card_no = form.id_card_no.data
            user.phone_no = form.phone_no.data
            user.email = form.email.data
            user.remark = form.remark.data
            role_group = RoleGroup.query.filter_by(name="公司用户组").one()
            user.role_id = role_group.role_id
            user.is_active = False
            user.user_type = UserType.COPR_CUSTOMER
            user.agency_id = agency.agency_id
            db.session.add(user)
            try:
                db.session.commit()
                return redirect(url_for('admin.corp_customers'))
            except IntegrityError as error:
                db.session.rollback()
                flash('同名账户已经存在，不能添加', "error")

    return render_template("admin/common.html", form=form,
                           title="添加公司用户", nav_menu=get_nav_menu(current_user),
                           tab_menu=get_tab_menu("customers", current_user, "公司用户"))


@admin.route('/admin/mod-corp-customer/<user_id>',methods=['GET', 'POST'])
@login_required
def mod_corp_customer(user_id):
    """修改公司用户
    """
    form = ModifyCorpCustomerForm()
    user = User.query.filter_by(user_id=user_id).one()
    agency = user.agency
    if form.validate_on_submit():
        agency.corp_name = form.corp_name.data
        agency.corp_license_no = form.corp_license_no.data
        agency.sub_account_no = int(form.sub_account_no.data)
        db.session.add(agency)

        user.login_name = form.login_name.data
        user.name = form.name.data
        # user.id_card_no = form.id_card_no.data
        user.phone_no = form.phone_no.data
        user.email = form.email.data
        user.remark = form.remark.data
        db.session.add(user)

        try:
            db.session.commit()
            flash('公司用户已经修改')
            return redirect(url_for('admin.corp_customers'))
        except IntegrityError as error:
            db.session.rollback()
            flash('同名或同公司名冲突，不能修改', "error")

    form.login_name.data = user.login_name
    form.name.data = user.name
    # form.id_card_no.data = user.id_card_no
    form.phone_no.data = user.phone_no
    form.email.data = user.email
    form.remark.data = user.remark
    form.corp_name.data = agency.corp_name
    form.corp_license_no.data = agency.corp_license_no
    form.sub_account_no.data = agency.sub_account_no
    return render_template("admin/mod_corp_customer.html", form=form, user_id=user_id,
                           title="查看和修改公司用户资料", nav_menu=get_nav_menu(current_user),
                           tab_menu=get_tab_menu("customers", current_user, "公司用户"))


@admin.route('/admin/sub-corp-customers/<int:agency_id>',methods=['GET'])
@login_required
def sub_corp_customers(agency_id):
    """查看公司用户的子账户列表
    """
    agency = Agency.query.filter_by(agency_id=agency_id).one()
    sub_customers = agency.connected_users.filter_by(user_type=UserType.CORP_SUB_ACCOUNT).all()
    return render_template('admin/sub_corp_customers.html', sub_customers=sub_customers,
                           title="查看公司子账户", nav_menu=get_nav_menu(current_user),
                           tab_menu=get_tab_menu("customers", current_user, "公司用户"))


@admin.route('/admin/fee-records',methods=['GET'])
@login_required
def fee_records():
    """暂时展示用户的缴费记录
    """
    page = request.args.get('page', 1, type=int)
    pagination = FeeRecord.query.paginate(page, per_page=10, error_out=False)
    fees = pagination.items
    return render_template("admin/fee_records.html", fee_records=fees,pagination=pagination,
                           title="缴费记录", nav_menu=get_nav_menu(current_user),
                           tab_menu=get_tab_menu("customers", current_user, "缴费退费"))


def get_fee_start_date( customer_id ):
    """获取用户续费的起始日期
    """
    # 如果是新用户，没有缴费记录，则以今天为提示起始日期
    # 如果是缴费用户，则以最晚的缴费记录的expire_time为提示起始日期
    last_fee_record = FeeRecord.query.filter_by(customer_id=customer_id). \
        filter_by(is_valid=True). \
        order_by(FeeRecord.expire_time.desc()).first()

    if not last_fee_record:
        fee_start_time = datetime.datetime.now()
    else:
        fee_start_time = last_fee_record.expire_time + datetime.timedelta(days=1)

    return fee_start_time

def get_fee_expire_date( start_date, fee_id, charge_count ):
    """给出起始日期，收费类型和数量，计算截止日期
    """
    fee = Fee.query.filter_by(fee_id=fee_id).one()
    if fee.time_length_type == TimeLengthType.MONTHS:
        expire_date = start_date + relativedelta(months=1, days=-1)
    elif fee.time_length_type == TimeLengthType.DAYS:
        expire_date = start_date + datetime.timedelta(days=charge_count * fee.time_length - 1)
    else:
        raise ValueError()
    return expire_date


@admin.route('/admin/fee-span')
@login_required
def get_fee_span():
    """根据fee类型，起始日期，计算出终止日期
    """
    fee_id = request.args.get('fee_id', 1, type=int)
    charge_count = request.args.get('charge_count', 1, type=int)
    start_date_str = request.args.get('start_date', datetime.date.today().strftime("%Y-%m-%d"), type=str)
    start_date = datetime.datetime.strptime(start_date_str,"%Y-%m-%d")
    expire_date = get_fee_expire_date( start_date, fee_id, charge_count )
    return jsonify({
        'start_date': start_date.strftime("%Y-%m-%d"),
        'expire_date': expire_date.strftime("%Y-%m-%d")
    })


def validate_time_span( customer_id, start_date, expire_date ):
    """给出即将付费的时段，检查是否和已经付费的时段有重合，如果有则非法
    如果付费时段已经过期，也非法
    """
    start_time = datetime.datetime(start_date.year,start_date.month,start_date.day)
    expire_time = datetime.datetime(expire_date.year,expire_date.month,expire_date.day)
    fee_records = FeeRecord.query.filter_by(customer_id=customer_id). \
        filter_by(is_valid=True).all()

    for record in fee_records:
        if record.start_time <= start_time and record.expire_time >= start_time:
            return False

    for record in fee_records:
        if record.start_time <= expire_time and record.expire_time >= expire_time:
            return False

    today = datetime.date.today()
    today_time = datetime.datetime(today.year,today.month,today.day)
    if start_time<today_time or expire_time<today_time:
        return False

    return True

    # 下面这段有问题，以后再访
    # fee_records = FeeRecord.query.filter_by(customer_id=customer_id). \
    #     filter_by(is_valid=True). \
    #     filter_by(FeeRecord.start_time <= start_time). \
    #     filter_by(FeeRecord.start_time >= expire_time).all()

@admin.route('/admin/charge-fee/<int:customer_id>',methods=['GET', 'POST'])
@login_required
def charge_fee(customer_id):
    """记录用户缴费

       这里有个大bug，如果用户缴费不连续，那么中间的空挡期访问控制成问题了！！所以还得用RecordHistory来
       控制，在登录的时候进行详细验证。
       在User Table里面还是不加入expire_time为好！！
    """
    fee_records = FeeRecord.query.filter_by(customer_id=customer_id). \
        filter_by(is_valid=True).\
        order_by(FeeRecord.expire_time.desc()).all()

    form = ChargeFeeForm()
    if form.validate_on_submit():
        fee_id = form.fee.data
        start_date = form.start_date.data
        expire_date = get_fee_expire_date(start_date, fee_id, 1)
        if validate_time_span(customer_id, start_date, expire_date):
            fee_record = FeeRecord()
            fee_record.customer_id = customer_id
            fee_record.fee_id = form.fee.data
            fee_record.collector_id = current_user.user_id
            fee_record.start_time = form.start_date.data
            fee_record.expire_time = form.expire_date.data
            db.session.add(fee_record)
            db.session.commit()
            flash('收费已经添加')
            return redirect(url_for('admin.charge_fee',customer_id=customer_id))
        else:
            flash('付费时段有问题，请重新选择')

    if request.method == "GET":
        fee_start_time = get_fee_start_date(customer_id)
        form.start_date.data = fee_start_time
        form.expire_date.data = get_fee_expire_date(fee_start_time, form.fee.choices[0][0], 1)

    return render_template("admin/charge_fee.html", form=form, fee_records=fee_records,
                           title="用户缴费", nav_menu=get_nav_menu(current_user),
                           tab_menu=get_tab_menu("customers", current_user, "缴费退费"))


@admin.route('/admin/fee-standards',methods=['GET'])
@login_required
def fee_standards():
    """查看收费标准
    """
    fees = Fee.query.all()
    return render_template('admin/fee_standards.html', fees=fees,
                           title="查看收费标准", nav_menu=get_nav_menu(current_user),
                           tab_menu=get_tab_menu("customers", current_user, "收费标准"))


@admin.route('/admin/add-fee-standard',methods=['GET', 'POST'])
@login_required
def add_fee_standard():
    """添加收费标准
    """
    form = AddFeeStandardForm()
    if form.validate_on_submit():
        fee = Fee()
        fee.fee_name = form.fee_name.data
        fee.amount = form.amount.data
        fee.time_length = form.time_length.data
        fee.time_length_type = form.time_length_type.data
        fee.discount = form.discount.data
        fee.tickets_no = form.tickets_no.data
        db.session.add(fee)
        try:
            db.session.commit()
            flash('收费标准已经添加')
            return redirect(url_for('admin.fee_standards'))
        except IntegrityError as error:
            db.session.rollback()
            flash('同名的收费标准已经存在，请另外取名', "error")
    return render_template("admin/common.html", form=form,
                           title="添加收费标准", nav_menu=get_nav_menu(current_user),
                           tab_menu=get_tab_menu("customers", current_user, "收费标准"))

# 应该还有个删除收费标准