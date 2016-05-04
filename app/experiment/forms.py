#from flask.ext.wtf import Form
from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
# from ..models import User


class LoginForm(Form):
    login_name = StringField('账号', validators=[Required('请输入账号'), Length(1, 64)])
    password = PasswordField('密码', validators=[Required('请输入密码')])
    start_time = DateField('起始时间',id="datepicker")
    remember_me = BooleanField('保持登录')
    submit = SubmitField('登录')


class DateForm(Form):
    start_time = DateField('选择日期',id="datepicker", format='%Y-%m-%d')
    submit = SubmitField('提交')