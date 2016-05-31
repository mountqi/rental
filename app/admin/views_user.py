"""
后台首页
后台管理员
后台权限组
"""
from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, \
    current_user
from sqlalchemy.exc import IntegrityError

from . import admin
from .forms_user import ChangeAdminUserInforForm, ChangePasswordForm, ModifyAdminUserForm,\
    AddAdminUserForm, AddModRoleGroupForm

from .. import db, check_empty
from ..models_user import User, RoleGroup, UserType, Permission
from .menu_factory import get_nav_menu, get_tab_menu
from ..decorators import permission_required
from ..utils import strip

@admin.route('/')
@login_required
def home():
    """首页
    """
    if current_user.is_backend_admin():
        return redirect(url_for('admin.index'))
    else:
        return redirect(url_for('customer.index'))



@admin.route('/admin')
@login_required
def index():
    """后台管理首页
    """
    return render_template("admin/index.html",
                           nav_menu=get_nav_menu(current_user),
                           title="后台首页")


@admin.route('/admin-undone')
@login_required
def undone():
    """后台管理未完成页面
    """
    return render_template("admin/undone.html",
                           nav_menu=get_nav_menu(current_user),
                           title="工作待完成")


@admin.route('/admin/user-self-update',methods=['GET', 'POST'])
@login_required
def user_self_update():
    """后台用户更新自己的信息
    """
    form = ChangeAdminUserInforForm()
    if form.validate_on_submit():
        current_user.name = strip(form.name.data)
        current_user.phone_no = strip(form.phone_no.data)
        current_user.email = strip(form.email.data)
        db.session.add(current_user)
        db.session.commit()
        flash('您的个人信息已经更新')
        return redirect( url_for('admin.user_self_update') )

    form.name.data = check_empty(current_user.name)
    form.phone_no.data = check_empty(current_user.phone_no)
    form.email.data = check_empty(current_user.email)
    return render_template('admin/user_self_update.html', form=form, \
                           title="修改个人信息", nav_menu=get_nav_menu(current_user))


@admin.route('/admin/user-self-passwd',methods=['GET', 'POST'])
@login_required
def user_self_passwd():
    """后台用户更新自己的密码
    """
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(strip(form.old_password.data)):
            current_user.password = strip(form.password.data)
            db.session.add(current_user)
            flash('您的密码已经更新')
            return redirect(url_for('admin.user'))
        else:
            flash('旧密码输入错误','warning')
    return render_template("admin/user_self_passwd.html", form=form, \
                           title="修改个人密码", nav_menu=get_nav_menu(current_user))


@admin.route('/admin/users',methods=['GET'])
@login_required
@permission_required(Permission.ADD_MOD_ADMIN_USER)
def users():
    """后台用户列表
    """
    page = request.args.get('page', 1, type=int)
    pagination = User.query.filter_by(user_type=UserType.BACKEND_ADMIN).paginate(
        page, per_page=10, error_out=False)
    all_users = pagination.items
    return render_template('admin/users.html', users=all_users, pagination=pagination,
                           title="查看后台管理员", nav_menu=get_nav_menu(current_user),\
                           tab_menu=get_tab_menu("users",current_user,"管理员"))


@admin.route('/admin/add-user',methods=['GET', 'POST'])
@login_required
@permission_required(Permission.ADD_MOD_ADMIN_USER)
def add_user():
    """添加后台用户
    """
    form = AddAdminUserForm()
    if form.validate_on_submit():
        user = User()
        user.login_name = strip(form.login_name.data)
        user.name = strip(form.name.data)
        user.password = strip(form.password.data)
        user.phone_no = strip(form.phone_no.data)
        user.email = strip(form.email.data)
        user.remark = strip(form.remark.data)
        user.role_id = form.role.data
        user.is_active = form.status.data
        user.user_type = UserType.BACKEND_ADMIN
        db.session.add(user)
        try:
            db.session.commit()
            flash('管理员已经添加')
            return redirect(url_for('admin.users'))
        except IntegrityError as error:
            db.session.rollback()
            flash('用户名已经存在，添加失败', "error")

    return render_template("admin/common.html", form=form,
                           title="添加后台管理员", nav_menu=get_nav_menu(current_user),
                           tab_menu=get_tab_menu("users", current_user, "管理员"))


@admin.route('/admin/mod-user/<user_id>',methods=['GET', 'POST'])
@login_required
@permission_required(Permission.ADD_MOD_ADMIN_USER)
def mod_user(user_id):
    """查看和修改后台用户信息
    """
    form = ModifyAdminUserForm()
    user = User.query.filter_by(user_id=user_id).one()
    if form.validate_on_submit():
        user.login_name = strip(form.login_name.data)
        user.name = strip(form.name.data)
        user.phone_no = strip(form.phone_no.data)
        user.email = strip(form.email.data)
        user.remark = strip(form.remark.data)
        user.role_id = form.role.data
        user.is_active = form.status.data
        db.session.add(user)
        db.session.commit()
        flash('用户信息已经更新')
        return redirect( url_for('admin.mod_user',user_id=user_id) )

    form.login_name.data = user.login_name
    form.name.data = check_empty(user.name)
    form.phone_no.data = check_empty(user.phone_no)
    form.email.data = check_empty(user.email)
    form.remark.data = check_empty(user.remark)
    form.role.data = user.role_id
    form.status.data = user.is_active
    new_passwd_next = url_for('admin.mod_user',user_id=user_id)
    return render_template("admin/mod_user.html", form=form,user_id=user_id,new_passwd_next=new_passwd_next,
                           title="查看和修改后台管理员资料", nav_menu=get_nav_menu(current_user),\
                           tab_menu=get_tab_menu("users",current_user,"管理员"))


@admin.route('/admin/rolegroups',methods=['GET'])
@login_required
@permission_required(Permission.ADD_MOD_PMSN_GRP)
def rolegroups():
    """查看用户组列表
    """
    page = request.args.get('page', 1, type=int)
    pagination = RoleGroup.query.paginate( page, per_page=10, error_out=False)
    role_groups = pagination.items
    return render_template('admin/rolegroups.html', role_groups=role_groups,
                           pagination=pagination, title="查看权限组",
                           nav_menu=get_nav_menu(current_user),
                           tab_menu=get_tab_menu("users", current_user, "权限组"))


@admin.route('/admin/add-rolegroup',methods=['GET', 'POST'])
@login_required
@permission_required(Permission.ADD_MOD_PMSN_GRP)
def add_rolegroup():
    """添加用户组
    """
    form = AddModRoleGroupForm()
    if form.validate_on_submit():
        rolegroup = RoleGroup()
        rolegroup.name = strip(form.name.data)
        rolegroup.remark = strip(form.remark.data)
        rolegroup.permissions = form.get_permissions()
        if rolegroup.permissions != 0:
            same_role_group_in_use = RoleGroup.query.filter_by(permissions=rolegroup.permissions).first()
            if same_role_group_in_use:
                flash('组权限与 {} 相同，不能冗余创建'.format(same_role_group_in_use.name), "error")
            else:
                db.session.add(rolegroup)
                try:
                    db.session.commit()
                    flash('权限组已经添加')
                    return redirect(url_for('admin.rolegroups'))
                except IntegrityError as error:
                    db.session.rollback()
                    flash('同名权限组已经存在，请另外取名', "error")
        else:
            flash('没有为权限组设置权限',"error")
    return render_template("admin/add_mod_rolegroups.html", form=form, title="添加权限组",
                           nav_menu=get_nav_menu(current_user),
                           tab_menu=get_tab_menu("users", current_user, "权限组"))


@admin.route('/admin/mod-rolegroup/<int:role_id>',methods=['GET', 'POST'])
@login_required
@permission_required(Permission.ADD_MOD_PMSN_GRP)
def mod_rolegroup(role_id):
    """查看和修改用户组
    """
    form = AddModRoleGroupForm()
    rolegroup = RoleGroup.query.filter_by(role_id=role_id).one()
    if form.validate_on_submit():
        rolegroup.name = strip(form.name.data)
        rolegroup.remark = strip(form.remark.data)
        if form.get_permissions() != 0:
            same_role_group_in_use = RoleGroup.query.filter_by(permissions=form.get_permissions()).first()
            if same_role_group_in_use:
                flash('组权限与 {} 相同，不能设置相同权限的组'.format(same_role_group_in_use.name), "error")
            else:
                rolegroup.permissions = form.get_permissions()
                db.session.add(rolegroup)
                db.session.commit()
                flash('权限组已经修改')
                return redirect(url_for('admin.rolegroups'))
        else:
            flash('没有为权限组设置权限',"error")

    if request.method == "GET":
        form.name.data = rolegroup.name
        form.remark.data = rolegroup.remark
        form.set_permissions(rolegroup.permissions)
    return render_template("admin/add_mod_rolegroups.html", form=form, title="查看和修改权限组",
                           nav_menu=get_nav_menu(current_user),
                           tab_menu=get_tab_menu("users", current_user, "权限组"))