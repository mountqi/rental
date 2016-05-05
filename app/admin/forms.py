from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField, \
    SelectField, TextAreaField, IntegerField, FloatField, DateField
from wtforms.validators import Required, DataRequired, InputRequired, \
    Length, Email, Regexp, EqualTo, Optional, NumberRange
from wtforms import ValidationError
from ..user_models import RoleGroup, Permission, Fee, TimeLengthType


class ServerRequired(object):
    """
    """
    def __init__(self, message=None):
        self.message = message

    def __call__(self, form, field):
        print("ServerRequired called")
        data = str(field.data).strip()
        if len(data) == 0:
            raise ValidationError(self.message)


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


class AddPersonalUserForm(Form):
    login_name = StringField('账号（*）', validators=[Length(11,11,"用户名必须为11位长度的手机号码"),
                                                  Regexp('[0-9]', 0, "手机号码格式不正确")])
    name = StringField('姓名（*）', validators=[ServerRequired('姓名不能为空'), Length(1, 32, "长度1-32字符")])
    password = PasswordField('密码（*）', validators=[ServerRequired('密码不能为空'), Length(8, 32, "长度8-32字符")] )
    phone_no = StringField('电话（*）', validators=[ServerRequired('电话号码必填'), Length(1, 20, "长度最大20位"),
                                                Regexp('[0-9-]', 0, "电话号码格式不正确")])
    email = StringField('邮箱', validators=[Optional(), Length(1, 64, "长度最大64"),
                                          Email("邮箱地址不正确")])
    remark = TextAreaField('备注', validators=[Optional(), Length(0, 64, "长度最大120字符")])
    submit = SubmitField('添加')


class ModifyPersonalUserForm(Form):
    login_name = StringField('账号（*）', validators=[Length(11, 11, "用户名必须为11位长度的手机号码"),
                                                  Regexp('[0-9]', 0, "手机号码格式不正确")])
    name = StringField('姓名（*）', validators=[ServerRequired('姓名不能为空'), Length(1, 32, "长度1-32字符")])
    phone_no = StringField('电话（*）', validators=[ServerRequired('电话号码必填'), Length(1, 20, "长度最大20位"),
                                                Regexp('[0-9-]', 0, "电话号码格式不正确")])
    email = StringField('邮箱', validators=[Optional(), Length(1, 64, "长度最大64"),
                                          Email("邮箱地址不正确")])
    remark = TextAreaField('备注', validators=[Optional(), Length(0, 120, "长度最大120字符")])
    submit = SubmitField('提交修改')


# for the super-admin to change other's password
class ChangeUserPasswordForm(Form):
    password = PasswordField('请输入新密码', validators=[
        ServerRequired('新密码不能为空'), EqualTo('password2', message='新密码两次输入必须相同'),
        Length(8, 32, "长度8-32字符")])
    password2 = PasswordField('请再次输入新密码', validators=[ServerRequired('新密码不能为空')])
    submit = SubmitField('更改密码')


class AddCorpCustomerForm(Form):
    login_name = StringField('账号（*）', validators=[Length(11, 11, "用户名必须为11位长度的手机号码"),
                                                  Regexp('[0-9]', 0, "手机号码格式不正确")])
    name = StringField('姓名（*）', validators=[ServerRequired('姓名不能为空'), Length(1, 32, "长度1-32字符")])
    password = PasswordField('密码（*）', validators=[ServerRequired('密码不能为空'), Length(8, 32, "长度8-32字符")])
    # id_card_no = StringField('身份证号码', validators=[Optional(), Length(18, 18, "身份证号码必须18位"),
    #                                               Regexp('[0-9A-Z]', 0, "身份证号码格式不正确")])
    phone_no = StringField('电话（*）', validators=[ServerRequired('电话号码必填'), Length(1, 20, "长度最大20位"),
                                                Regexp('[0-9-]', 0, "电话号码格式不正确")])
    email = StringField('邮箱', validators=[Optional(), Length(1, 64, "长度最大64"),
                                          Email("邮箱地址不正确")])
    corp_name = StringField('公司全称（*）', validators=[ServerRequired('公司名称不能为空'), Length(1, 32, "长度1-32字符")])
    corp_license_no = StringField('营业执照号码', validators=[Optional(), Length(1, 64, "长度最大64")])
    sub_account_no = IntegerField('子账户数量（*）', validators=[ServerRequired('必须设定最大子账户数量'),
                                                          NumberRange(1, 100, "子账户数量必须大于0")])
    remark = TextAreaField('备注', validators=[Optional(), Length(0, 120, "长度最大120字符")])
    submit = SubmitField('添加')


class ModifyCorpCustomerForm(Form):
    login_name = StringField('账号（*）', validators=[Length(11, 11, "用户名必须为11位长度的手机号码"),
                                                  Regexp('[0-9]', 0, "手机号码格式不正确")])
    name = StringField('姓名（*）', validators=[ServerRequired('姓名不能为空'),
                                        Length(1, 32, "长度1-32字符")])
    # id_card_no = StringField('身份证号码')
    phone_no = StringField('电话（*）', validators=[ServerRequired('电话号码必填'), Length(1, 20, "长度最大20位"),
                                                Regexp('[0-9-]', 0, "电话号码格式不正确")])
    email = StringField('邮箱', validators=[Optional(), Length(1, 64, "长度最大64"),
                                          Email("邮箱地址不正确")])
    corp_name = StringField('公司全称（*）', validators=[ServerRequired('公司名称不能为空'), Length(1, 32, "长度1-32字符")])
    corp_license_no = StringField('营业执照号码', validators=[Optional(), Length(1, 64, "长度最大64")])
    sub_account_no = IntegerField('子账户数量（*）', validators=[ServerRequired('必须设定最大子账户数量'),
                                                          NumberRange(1, 100, "子账户数量必须大于0")])
    remark = TextAreaField('备注', validators=[Optional(), Length(0, 120, "长度最大120字符")])
    submit = SubmitField('提交修改')


class AddFeeStandardForm(Form):
    fee_name = StringField('标准名称', validators=[ Length(1, 64, "名称长度1到15个字符")])
    time_length = IntegerField('时间长度')
    time_length_type = SelectField('时间长度单位', coerce=int)
    amount = IntegerField('额度', validators=[ServerRequired('额度不能为空')])
    discount = FloatField('折扣', validators=[ServerRequired('折扣不能为空'),
                                            NumberRange(0.0,1.0,"折扣区间0到1")])
    tickets_no = IntegerField('每日查看房东联系方式数量', validators=[ServerRequired('数量不能为空')])
    submit = SubmitField('添加')

    def __init__(self, *args, **kwargs):
        super(AddFeeStandardForm, self).__init__(*args, **kwargs)
        self.time_length_type.choices = [(TimeLengthType.MONTHS, "月"), (TimeLengthType.DAYS, "天")]


class ChargeFeeForm(Form):
    start_date = DateField('选择日期', id="start-date", format='%Y-%m-%d')
    expire_date = DateField('终止时间', id="expire-date")
    fee = SelectField('收费标准', id="fee-standard", coerce=int)
    submit = SubmitField('提交')

    def __init__(self, *args, **kwargs):
        super(ChargeFeeForm, self).__init__(*args, **kwargs)
        self.fee.choices = [(fee.fee_id, fee.fee_name)
                             for fee in Fee.query.all()]


