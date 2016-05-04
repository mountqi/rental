"""
前端个人用户
前端公司用户
收费
"""
import datetime
from sqlalchemy.exc import IntegrityError
from sqlalchemy import and_, or_, not_
from flask import render_template, redirect, request, url_for, flash
from flask_login import login_required, current_user

from . import admin
from .forms import AddPersonalUserForm, ModifyPersonalUserForm,ChangeUserPasswordForm, \
    AddCorpCustomerForm, ModifyCorpCustomerForm, AddFeeStandardForm, ChargeFeeForm

from .. import db, check_empty
from ..user_models import User, UserType, Agency, Fee, FeeRecord, RoleGroup
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


@admin.route('/admin/charge-fee-tmp/<int:customer_id>',methods=['GET', 'POST'])
@login_required
def charge_fee_tmp(customer_id):
    """记录用户缴费
    """
    fee_records = FeeRecord.query.filter_by(customer_id=customer_id).all()
    form = ChargeFeeForm()
    if form.validate_on_submit():
        fee_record = FeeRecord()
        fee_record.customer_id = customer_id
        fee_record.fee_id = form.fee.data
        fee_record.collector_id = current_user.user_id
        fee_record.start_time = form.start_time.data
        db.session.add(fee_record)
        db.session.commit()
        flash('收费已经添加')
        return redirect(url_for('admin.charge_fee_tmp',customer_id=customer_id))

    if request.method == "GET":
        form.start_time.data = datetime.date.today()
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