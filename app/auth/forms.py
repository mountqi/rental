#from flask.ext.wtf import Form
from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo, Optional
from wtforms import ValidationError
from ..models_user import User
from ..utils import ServerRequired


class LoginForm(Form):
    login_name = StringField('账号', validators=[Required('请输入账号'), Length(1, 64)])
    password = PasswordField('密码', validators=[Required('请输入密码')])
    remember_me = BooleanField('保持登录')
    submit = SubmitField('登录')


class FindPasswdForm(Form):
    email = StringField('邮箱', validators=[Required('请输入邮箱'), Length(1, 64), Email("邮箱地址不正确")])
    submit = SubmitField('找回密码')


class PasswordResetForm(Form):
    email = StringField('您注册用的邮箱', validators=[ServerRequired('邮箱必填'), Length(1, 64),Email()])
    password = PasswordField('新密码', validators=[
        ServerRequired('密码不能为空') ])
    password2 = PasswordField('请确认新密码', validators=[ EqualTo('password', message='新密码两次输入必须相同')])
    submit = SubmitField('重置密码')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() is None:
            raise ValidationError('未知的邮箱地址')


class RegisterPersonalCustomerForm(Form):
    login_name = StringField('账号（*）', validators=[Length(11,11,"用户名必须为11位长度的手机号码"),
                                                  Regexp('[0-9]', 0, "手机号码格式不正确")])
    password = PasswordField('密码（*）', validators=[ServerRequired('密码不能为空'), Length(8, 32, "长度8-32字符")] )
    password2 = PasswordField('再次输入密码（*）', validators=[ServerRequired('密码不能为空'), Length(8, 32, "长度8-32字符"),
                                                       EqualTo('password', message='新密码两次输入必须相同')] )
    name = StringField('姓名（*）', validators=[ServerRequired('姓名不能为空'), Length(1, 32, "长度1-32字符")])
    idcard_no = StringField('证件号码', validators=[ Length(1, 32, "长度1-32字符")])
    email = StringField('邮箱', validators=[Optional(), Length(1, 64, "长度最大64"), Email("邮箱地址不正确")])
    submit = SubmitField('注册')


class RegisterCorpCustomerForm(Form):
    login_name = StringField('账号（*）', validators=[Length(11, 11, "用户名必须为11位长度的手机号码"),
                                          Regexp('[0-9]', 0, "手机号码格式不正确")])
    password = PasswordField('密码（*）', validators=[ServerRequired('密码不能为空'), Length(8, 32, "长度8-32字符")] )
    password2 = PasswordField('再次输入密码（*）', validators=[ Length(8, 32, "长度8-32字符"),
                                                       EqualTo('password', message='新密码两次输入必须相同')] )
    name = StringField('姓名（*）', validators=[ServerRequired('姓名不能为空'), Length(1, 32, "长度1-32字符")])
    corp_name = StringField('公司全称（*）', validators=[ServerRequired('公司名称不能为空'), Length(1, 32, "长度1-32字符")])
    corp_license_no = StringField('营业执照号码', validators=[Optional(), Length(1, 64, "长度最大64")])
    email = StringField('邮箱', validators=[Optional(), Length(1, 64, "长度最大64"), Email("邮箱地址不正确")])
    submit = SubmitField('注册')