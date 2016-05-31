from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField, \
    SelectField, TextAreaField, IntegerField, FloatField, DateField
from wtforms.validators import Required, DataRequired, InputRequired, \
    Length, Email, Regexp, EqualTo, Optional, NumberRange
from flask import render_template, redirect, request, url_for, flash

from ..models_property import City, District, Area, Estate, PropertyType, PropertySource
from ..utils import ServerRequired

# ---------- City --------------------------
class AddCityForm(Form):
    city_name = StringField('城市名称（*）', validators=[Length(1, 16, "长度1-16")])
    city_no   = StringField('电话区号（*）', validators=[Length(1, 8, "长度1-8"),
                                                   Regexp('[0-9]', 0, "电话区号格式不正确")])
    submit = SubmitField('添加')

# ---------- District --------------------------
class AddDistrictForm(Form):
    district_name = StringField('区县名称（*）', validators=[Length(1, 16, "长度1-16")])
    submit = SubmitField('添加')


class ShowCityListForDistrictForm(Form):
    city = SelectField('城市', id="city_selection")

    def __init__(self, *args, **kwargs):
        super(ShowCityListForDistrictForm, self).__init__(*args, **kwargs)
        self.city.choices = [(url_for('admin.districts', city_id=city.city_id), city.city_name)
                             for city in City.query.all()]

        self.city.data = url_for('admin.districts', city_id=kwargs['city_id'])

# ---------- Area --------------------------
class AddAreaForm(Form):
    area_name = StringField('区域名称（*）', validators=[Length(1, 16, "长度1-16")])
    submit = SubmitField('添加')


class ShowCityListForAreaForm(Form):
    city = SelectField('城市', id="city_selection")

    def __init__(self, *args, **kwargs):
        super(ShowCityListForAreaForm, self).__init__(*args, **kwargs)
        self.city.choices = [(url_for('admin.areas', city_id=city.city_id), city.city_name)
                             for city in City.query.all()]

        self.city.data = url_for('admin.areas', city_id=kwargs['city_id'])

# ---------- Estate --------------------------

def create_admin_estate_url( city_id, district_id, area_id ):
    return url_for('admin.estates', city_id=city_id, district_id=district_id, area_id=area_id)


class ShowCityListForAdminEstateForm(Form):
    city = SelectField('城市', id="city_selection")

    def __init__(self, *args, **kwargs):
        super(ShowCityListForAdminEstateForm, self).__init__(*args, **kwargs)
        city_id = kwargs['city_id']
        district_id = kwargs['district_id']
        area_id = kwargs['area_id']
        self.city.choices = [(create_admin_estate_url(city.city_id,district_id,area_id), city.city_name)
                             for city in City.query.all()]
        self.city.data = create_admin_estate_url( city_id, district_id, area_id )


class ShowDistrictListForAdminEstateForm(Form):
    district = SelectField('区县', id="district_selection")

    def __init__(self, *args, **kwargs):
        super(ShowDistrictListForAdminEstateForm, self).__init__(*args, **kwargs)
        city_id = kwargs['city_id']
        district_id = kwargs['district_id']
        area_id = kwargs['area_id']
        self.district.choices = [(create_admin_estate_url(city_id,district.district_id,area_id), district.district_name)
                             for district in District.query.filter_by(city_id=city_id).all()]
        item_all = (create_admin_estate_url( city_id, 0, area_id ),"--所有--")
        self.district.choices.insert(0,item_all)
        if district_id==0:
            self.district.data = item_all[0]
        else:
            self.district.data = create_admin_estate_url( city_id, district_id, area_id )


class ShowAreaListForAdminEstateForm(Form):
    area = SelectField('区域', id="area_selection")

    def __init__(self, *args, **kwargs):
        super(ShowAreaListForAdminEstateForm, self).__init__(*args, **kwargs)
        city_id = kwargs['city_id']
        district_id = kwargs['district_id']
        area_id = kwargs['area_id']
        self.area.choices = [(create_admin_estate_url(city_id,district_id,area.area_id), area.area_name)
                             for area in Area.query.filter_by(city_id=city_id).all()]
        # self.area.data = create_admin_estate_url( city_id, district_id, area_id )

        item_all = (create_admin_estate_url(city_id, district_id, 0), "--所有--")
        self.area.choices.insert(0, item_all)
        if area_id == 0:
            self.area.data = item_all[0]
        else:
            self.area.data = create_admin_estate_url(city_id, district_id, area_id)


class AddModEstateForm(Form):
    estate_name = StringField('楼盘/小区名称（*）', validators=[Length(1, 32, "长度1-32")])
    district = SelectField('区县（*）', coerce=int)
    area = SelectField('区域', coerce=int)
    english_name = StringField('英文名称', validators=[Optional(), Length(1, 64, "长度1-64")])
    zhpy = StringField('中文拼音首字母', validators=[Optional(), Length(1, 16, "长度1-16")])
    complete_year = StringField('建成时间', validators=[Optional(), Length(1, 8, "长度1-8")])
    address = StringField('地址（*）', validators=[Length(1, 64, "长度1-64")])
    developer = StringField('开发商', validators=[Optional(), Length(1, 32, "长度1-32")])
    mgt_company = StringField('物业公司', validators=[Optional(), Length(1, 32, "长度1-32")])
    # property_type = SelectField('房产类型', coerce=int)
    mgt_fee = IntegerField('每月物业费（单位：元）', validators=[Optional()])
    total_sqare = FloatField('建筑面积（单位：平米）', validators=[Optional()])
    total_houses = IntegerField('房屋套数', validators=[Optional()])
    floor_area_ratio = FloatField('容积率', validators=[Optional()])
    parking_no = IntegerField('停车位数量', validators=[Optional()])
    green_rate = FloatField('绿化率', validators=[Optional()])
    introduction = TextAreaField('介绍', validators=[Optional(), Length(0, 120, "长度最大120字符")])
    submit = SubmitField('提交')

    def __init__(self, *args, **kwargs):
        super(AddModEstateForm, self).__init__(*args, **kwargs)
        city_id = kwargs['city_id']

        # 区县列表
        self.district.choices = [ (district.district_id, district.district_name)
                                 for district in District.query.filter_by(city_id=city_id).all()]

        # # 区域列表
        self.area.choices = [( area.area_id, area.area_name)
                             for area in Area.query.filter_by(city_id=city_id).all()]
        no_area = (0, "")
        self.area.choices.insert(0, no_area)

# ---------- Property --------------------------

def create_admin_property_url( url, city_id, district_id, estate_id,  area_id, source ):
    return url_for( url, city_id=city_id, district_id=district_id, estate_id=estate_id,
                   area_id=area_id, source=source)


class ShowCityListForAdminPropertyForm(Form):
    city = SelectField('城市', id="city_selection")

    def __init__(self, *args, **kwargs):
        super(ShowCityListForAdminPropertyForm, self).__init__(*args, **kwargs)
        city_id = kwargs['city_id']
        district_id = kwargs['district_id']
        estate_id = kwargs['estate_id']
        area_id = kwargs['area_id']
        source = kwargs['source']
        url = kwargs['url']
        self.city.choices = [(city.city_id, city.city_name)
                             for city in City.query.all()]
        self.city.data = city_id


class ShowDistrictListForAdminPropertyForm(Form):
    district = SelectField('区县', id="district_selection")

    def __init__(self, *args, **kwargs):
        super(ShowDistrictListForAdminPropertyForm, self).__init__(*args, **kwargs)
        city_id = kwargs['city_id']
        district_id = kwargs['district_id']
        self.district.choices = [ (district.district_id, district.district_name)
                             for district in District.query.filter_by(city_id=city_id).all()]
        item_all = ( 0,"--所有--")
        self.district.choices.insert(0,item_all)
        if district_id==0:
            self.district.data = item_all[0]
        else:
            self.district.data = str(district_id)


class ShowEstateListForAdminPropertyForm(Form):
    estate = SelectField('楼盘', id="estate_selection")

    def __init__(self, *args, **kwargs):
        super(ShowEstateListForAdminPropertyForm, self).__init__(*args, **kwargs)
        district_id = kwargs['district_id']
        estate_id = kwargs['estate_id']
        self.estate.choices = [( estate.estate_id, estate.estate_name)
                             for estate in Estate.query.filter_by(district_id=district_id).all()]
        item_all = ( district_id, "--所有--")
        self.estate.choices.insert(0,item_all)
        if district_id==0:
            self.estate.data = item_all[0]
        else:
            self.estate.data = str(estate_id)


class ShowAreaListForAdminPropertyForm(Form):
    area = SelectField('区域', id="area_selection")

    def __init__(self, *args, **kwargs):
        super(ShowAreaListForAdminPropertyForm, self).__init__(*args, **kwargs)
        city_id = kwargs['city_id']
        area_id = kwargs['area_id']
        self.area.choices = [( area.area_id, area.area_name)
                             for area in Area.query.filter_by(city_id=city_id).all()]

        item_all = (0, "--所有--")
        self.area.choices.insert(0, item_all)
        if area_id == 0:
            self.area.data = item_all[0]
        else:
            self.area.data = str(area_id)


class ShowSourceListForAdminPropertyForm(Form):
    source = SelectField('来源', id="source_selection")

    def __init__(self, *args, **kwargs):
        super(ShowSourceListForAdminPropertyForm, self).__init__(*args, **kwargs)
        source = kwargs['source']
        self.source.choices = [( s.source_name, s.source_name)
                             for s in PropertySource.query.all()]

        item_all = ("", "--所有--")
        self.source.choices.insert(0, item_all)
        if source == "":
            self.source.data = item_all[0]
        else:
            self.source.data = str(source)


class AddPropertyForm(Form):
    city = SelectField('城市', coerce=int, id="city_selection")
    district = SelectField('区县', coerce=int, id="district_selection")
    estate = SelectField('楼盘', coerce=int, id="estate_selection")
    area = SelectField('区域', coerce=int, id="area_selection")
    build_no = StringField('楼栋号（*）', validators=[ ServerRequired('楼栋号必填'), Length(1, 16, "长度1-16")])
    floor = IntegerField('楼层（*）', validators=[ServerRequired('楼层必填')])
    floor_all = IntegerField('本栋楼总层数（*）', validators=[ServerRequired('本栋楼总层数必填')])
    room_no = StringField('房间号（*）', validators=[ServerRequired('房间号必填'),Length(1, 16, "长度1-16")])
    count_f = IntegerField('室', validators=[Optional()])
    count_t = IntegerField('厅', validators=[Optional()])
    count_w = IntegerField('卫', validators=[Optional()])
    count_y = IntegerField('阳台', validators=[Optional()])
    property_type = SelectField('类型')
    property_direction = StringField('朝向', validators=[Optional(), Length(1, 8, "长度1-8")])
    square = FloatField('面积（平米）', validators=[Optional()])
    owner_name = StringField('房东姓名', validators=[Optional(),Length(1, 16, "长度1-16")])
    contact_name = StringField('联系人', validators=[Optional(),Length(1, 16, "长度1-16")])
    contact_tel = StringField('联系电话', validators=[Optional(),Length(1, 32, "长度1-32")])
    status = SelectField('租房状态')
    inclusion = StringField('家具电器、发票、生活娱乐设施', validators=[Optional(),Length(1, 64, "长度1-64")])
    description = TextAreaField('说明', validators=[Optional(),Length(1, 256, "长度1-256")])
    valid_time = DateField('起租日期', id="valid-time", format='%Y-%m-%d', validators=[Optional()])
    trust_grade = IntegerField('可信度', validators=[Optional()])
    rent_price = FloatField('每月租金', validators=[Optional()])
    mgt_price = FloatField('每月物业费', validators=[Optional()])
    longitude = StringField('经度坐标', validators=[Optional(), Length(1, 24, "长度1-24")])
    latitude = StringField('维度坐标', validators=[Optional(), Length(1, 24, "长度1-24")])
    source = SelectField('房屋来源')
    submit = SubmitField('提交')

    def __init__(self, *args, **kwargs):
        super(AddPropertyForm, self).__init__(*args, **kwargs)

        # 城市列表
        city_id = kwargs['city_id']
        district_id = kwargs['district_id']
        estate_id = kwargs['estate_id']
        area_id = kwargs['area_id']
        source = kwargs['source']

        self.city.choices = [(c.city_id, c.city_name)
                                 for c in City.query.all()]
        self.city.data = city_id

        # 区县列表，这个取决于城市，但是初始化应该根据城市来
        self.district.choices = [(district.district_id, district.district_name)
                                 for district in District.query.filter_by(city_id=city_id).all()]

        # 楼盘列表，这个取决于行政区
        self.estate.choices = [(estate.estate_id, estate.estate_name)
                               for estate in Estate.query.filter_by(district_id=district_id).all()]
        if len(self.estate.choices)==0:
            no_estate = (0, "")
            self.estate.choices.insert(0, no_estate)

        # 区域列表
        self.area.choices = [(area.area_id, area.area_name)
                             for area in Area.query.filter_by(city_id=city_id).all()]
        no_area = (0, "")
        self.area.choices.insert(0, no_area)

        # 物业类型列表
        self.property_type.choices = [ (type.type_name, type.type_name)
            for type in PropertyType.query.all()]


        # 租房状态
        status_list = ["可租", "已租", "预定", "未知"]
        self.status.choices = [(s, s) for s in status_list]

        # 房屋来源
        self.source.choices = [ (s.source_name,s.source_name) for s in PropertySource.query.all()]






# ---------- Follow --------------------------
class AddFollowForm(Form):
    follow_content = TextAreaField('跟进内容（*）', validators=[Length(1, 128, "长度1-128")])
    submit = SubmitField('提交')
