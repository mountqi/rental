#from flask.ext.wtf import Form
from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
# from ..models import User

#
# class LoginForm(Form):
#     email = StringField('账号', validators=[Required('请输入账号'), Length(1, 64)])
#     password = PasswordField('密码', validators=[Required('请输入密码')])
#     submit = SubmitField('登录')
#
#
# class ChangePasswordForm(Form):
#     old_password = PasswordField('Old password', validators=[Required()])
#     password = PasswordField('New password', validators=[
#         Required(), EqualTo('password2', message='Passwords must match')])
#     password2 = PasswordField('Confirm new password', validators=[Required()])
#     submit = SubmitField('Update Password')

