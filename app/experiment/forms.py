#from flask.ext.wtf import Form
from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
# from ..models import User

from wtforms import StringField, PasswordField, BooleanField, SubmitField, \
    SelectField, TextAreaField, IntegerField, FloatField, DateField
from wtforms.validators import Required, DataRequired, InputRequired, \
    Length, Email, Regexp, EqualTo, Optional, NumberRange
from flask import render_template, redirect, request, url_for, flash

from ..models_property import City, District, Area, Estate, PropertyType


class LoginForm(Form):
    login_name = StringField('账号', validators=[Required('请输入账号'), Length(1, 64)])
    password = PasswordField('密码', validators=[Required('请输入密码')])
    submit = SubmitField('登录')


class DateForm(Form):
    start_time = DateField('选择日期',id="datepicker", format='%Y-%m-%d')
    expire_time = DateField('自动日期', id="date2", format='%Y-%m-%d')
    submit = SubmitField('提交')

class AddEstateForm(Form):
    estate_name = StringField('楼盘/小区名称（*）', validators=[Length(1, 32, "长度1-32")])
    district = SelectField('区县（*）', coerce=int)
    area = SelectField('区域', coerce=int)
    english_name = StringField('英文名称', validators=[Optional(), Length(1, 64, "长度1-64")])
    zhpy = StringField('中文拼音首字母', validators=[Optional(), Length(1, 16, "长度1-16")])
    complete_year = StringField('建成时间', validators=[Optional(), Length(1, 8, "长度1-8")])
    address = StringField('地址', validators=[Length(1, 64, "长度1-64")])
    developer = StringField('开发商', validators=[Optional(), Length(1, 32, "长度1-32")])
    mgt_company = StringField('物业公司', validators=[Optional(), Length(1, 32, "长度1-32")])
    property_type = SelectField('房产类型', coerce=int)
    mgt_fee = IntegerField('每月物业费（单位：元）', validators=[Optional()])
    total_sqare = FloatField('建筑面积（单位：平米）', validators=[Optional()])
    total_houses = IntegerField('房屋套数', validators=[Optional()])
    floor_area_ratio = FloatField('容积率', validators=[Optional()])
    parking_no = IntegerField('停车位数量', validators=[Optional()])
    green_rate = FloatField('绿化率', validators=[Optional()])
    introduction = TextAreaField('介绍', validators=[Optional(), Length(0, 120, "长度最大120字符")])
    submit = SubmitField('添加')

    def __init__(self, *args, **kwargs):
        super(AddEstateForm, self).__init__(*args, **kwargs)
        city_id = kwargs['city_id']

        # 区县列表
        self.district.choices = [(district.district_id, district.district_name)
                                 for district in District.query.filter_by(city_id=city_id).all()]

        # # 区域列表
        self.area.choices = [(area.area_id, area.area_name)
                             for area in Area.query.filter_by(city_id=city_id).all()]
        no_area = (0, "")
        self.area.choices.insert(0, no_area)

        # 物业类型列表
        self.property_type.choices = [(type, PropertyType.get_property_type_str(type))
                                      for type in PropertyType.get_property_type_list()]
