from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField, \
    SelectField, TextAreaField, IntegerField, FloatField, DateField
from wtforms.validators import Required, DataRequired, InputRequired, \
    Length, Email, Regexp, EqualTo, Optional, NumberRange

from ..models_user import RoleGroup, Permission, Fee, TimeLengthType
from ..utils import ServerRequired


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
    password2 = PasswordField('请再次输入新密码', validators=[ServerRequired('新密码不能为空'),
                                                      EqualTo('password', message='新密码两次输入必须相同')])
    submit = SubmitField('更改密码')


class AddCorpCustomerForm(Form):
    login_name = StringField('账号（*）', validators=[Length(11, 11, "用户名必须为11位长度的手机号码"),
                                                  Regexp('[0-9]', 0, "手机号码格式不正确")])
    name = StringField('姓名（*）', validators=[ServerRequired('姓名不能为空'), Length(1, 32, "长度1-32字符")])
    password = PasswordField('密码（*）', validators=[ServerRequired('密码不能为空'), Length(8, 32, "长度8-32字符")])
    id_card_no = StringField('证件号码', validators=[Optional(), Length(1, 32, "长度1-32字符")])
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
    start_date = DateField('选择缴费起始日', id="start-date", format='%Y-%m-%d')
    expire_date = DateField('终止日', id="expire-date")
    fee = SelectField('收费标准', id="fee-standard", coerce=int)
    submit = SubmitField('提交')

    def __init__(self, *args, **kwargs):
        super(ChargeFeeForm, self).__init__(*args, **kwargs)
        self.fee.choices = [(fee.fee_id, fee.fee_name)
                             for fee in Fee.query.all()]


