from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField, \
    SelectField, TextAreaField, IntegerField, FloatField, DateField
from wtforms.validators import Required, DataRequired, InputRequired, \
    Length, Email, Regexp, EqualTo, Optional, NumberRange

from ..models_user import RoleGroup, Permission, Fee, TimeLengthType
from ..utils import ServerRequired


class ChangeAdminUserInforForm(Form):
    name = StringField('姓名（*）', validators=[ServerRequired("请输入姓名"), Length(1, 64)])
    phone_no = StringField('电话', validators=[Optional(), Length(1, 20, "长度最大20位"),
                                             Regexp('[0-9-]', 0, "电话号码格式不正确")])
    email = StringField('邮箱', validators=[Optional(), Length(1, 64, "长度最大64"),
                                          Email("邮箱地址不正确")])
    submit = SubmitField('提交修改')


class ChangePasswordForm(Form):
    old_password = PasswordField('请输入旧密码（*）', validators=[ServerRequired("")])
    password = PasswordField('请输入新密码（*）', validators=[
        ServerRequired(""), EqualTo('password2', message='新密码两次输入必须相同'),
        Length(8, 32, "长度8-32字符")])
    password2 = PasswordField('请再次输入新密码（*）', validators=[ServerRequired("")])
    submit = SubmitField('更改密码')


class ModifyAdminUserForm(Form):
    login_name = StringField('账号（*）', validators=[Length(1, 64, "长度1-64")])
    name = StringField('姓名（*）', validators=[Length(1, 64, "长度1-64")])
    phone_no = StringField('电话', validators=[Optional(), Length(1, 20, "长度最大20位"),
                                             Regexp('[0-9-]', 0, "电话号码格式不正确")])
    email = StringField('邮箱', validators=[Optional(), Length(1, 64, "长度最大64"),
                                          Email("邮箱地址不正确")])
    role = SelectField('权限组', coerce=int)
    status = SelectField('状态', coerce=int)
    remark = TextAreaField('备注')
    submit = SubmitField('提交修改')

    def __init__(self, *args, **kwargs):
        super(ModifyAdminUserForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.role_id, role.name)
                             for role in RoleGroup.query.all()]
        self.status.choices = [(1,"启用"),(0,"停止")]


class AddAdminUserForm(Form):
    login_name = StringField('账号（*）', validators=[Length(1, 64, "长度1-64")])
    name = StringField('姓名（*）', validators=[Length(1, 64, "长度1-64")])
    password = PasswordField('密码（*）', validators=[Length(1, 64, "长度1-64")])
    phone_no = StringField('电话', validators=[Optional(), Length(1, 20, "长度最大20位"),
                                             Regexp('[0-9-]', 0, "电话号码格式不正确")])
    email = StringField('邮箱', validators=[Optional(), Length(1, 64, "长度最大64"),
                                          Email("邮箱地址不正确")])
    role = SelectField('权限组', coerce=int)
    status = SelectField('状态', coerce=int)
    remark = TextAreaField('备注')
    submit = SubmitField('添加')

    def __init__(self, *args, **kwargs):
        super(AddAdminUserForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.role_id, role.name)
                             for role in RoleGroup.query.all() if not
                             Permission.is_customer(role.permissions)]
        self.status.choices = [(1,"启用"),(0,"停止")]


class AddModRoleGroupForm(Form):
    name = StringField('权限组名', validators=[ServerRequired('组名不能为空'),
                                           Length(1, 64, "长度最大64")])
    remark = TextAreaField('备注信息', validators=[Optional(),Length(1, 64, "长度最大256")])
    add_mod_pmsn_grp = BooleanField('添加/配置权限组')
    add_mod_admin_user = BooleanField('添加/修改管理账户')
    backup_restore_data = BooleanField('数据备份/恢复')
    add_del_house = BooleanField('添加/删除房源')
    mod_house_info = BooleanField('修改房源信息')
    mod_house_status = BooleanField('更新房源状态')
    add_mod_customer = BooleanField('建立/更改用户')
    visit_house_info = BooleanField('房源基本信息访问')
    visit_house_contact = BooleanField('房源联系方式访问')
    follow_house_status = BooleanField('房源状态跟进')
    pre_add_house = BooleanField('添加待审核房源')
    submit = SubmitField('提交修改')

    def __init__(self, *args, **kwargs):
        super(AddModRoleGroupForm, self).__init__(*args, **kwargs)

    def set_permissions(self,permissions):
        self.add_mod_pmsn_grp.data      = permissions&Permission.ADD_MOD_PMSN_GRP
        self.add_mod_admin_user.data    = permissions&Permission.ADD_MOD_ADMIN_USER
        self.backup_restore_data.data   = permissions&Permission.BACKUP_RESTORE_DATA
        self.add_del_house.data         = permissions&Permission.ADD_DEL_HOUSE
        self.mod_house_info.data        = permissions&Permission.MOD_HOUSE_INFO
        self.mod_house_status.data      = permissions&Permission.MOD_HOUSE_STATUS
        self.add_mod_customer.data      = permissions&Permission.ADD_MOD_CUSTOMER
        self.visit_house_info.data      = permissions&Permission.VISIT_HOUSE_INFO
        self.visit_house_contact.data   = permissions&Permission.VISIT_HOUSE_CONTACT
        self.follow_house_status.data   = permissions&Permission.FOLLOW_HOUSE_STATUS
        self.pre_add_house.data         = permissions&Permission.PRE_ADD_HOUSE

    def get_permissions(self):
        permissions = 0
        if self.add_mod_pmsn_grp.data      : permissions |= Permission.ADD_MOD_PMSN_GRP
        if self.add_mod_admin_user.data    : permissions |= Permission.ADD_MOD_ADMIN_USER
        if self.backup_restore_data.data   : permissions |= Permission.BACKUP_RESTORE_DATA
        if self.add_del_house.data         : permissions |= Permission.ADD_DEL_HOUSE
        if self.mod_house_info.data        : permissions |= Permission.MOD_HOUSE_INFO
        if self.mod_house_status.data      : permissions |= Permission.MOD_HOUSE_STATUS
        if self.add_mod_customer.data      : permissions |= Permission.ADD_MOD_CUSTOMER
        if self.visit_house_info.data      : permissions |= Permission.VISIT_HOUSE_INFO
        if self.visit_house_contact.data   : permissions |= Permission.VISIT_HOUSE_CONTACT
        if self.follow_house_status.data   : permissions |= Permission.FOLLOW_HOUSE_STATUS
        if self.pre_add_house.data         : permissions |= Permission.PRE_ADD_HOUSE
        return permissions


