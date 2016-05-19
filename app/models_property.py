from datetime import datetime, timedelta
import hashlib
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from markdown import markdown
import bleach
from flask import current_app, request, url_for
from flask_login import UserMixin, AnonymousUserMixin
from app.exceptions import ValidationError
from . import db

"""
City 查看/修改
District 查看/修改
Area 查看/修改
Estate 查看/修改
House 查看/修改
Follow 查看/添加
Resource 生活设施、运动、商场、学校，每个单位都要加上地址
image

"""

# class PropertyType:
#     HOUSE = 0
#     VILLA = 1
#     APARTMENT = 2
#
#     @staticmethod
#     def get_property_type_list():
#         return (PropertyType.HOUSE, PropertyType.VILLA, PropertyType.APARTMENT)
#
#     @staticmethod
#     def get_property_type_str(type):
#         return { PropertyType.HOUSE:"住房", PropertyType.VILLA:"别墅", PropertyType.APARTMENT:"公寓" }[type]

class PropertyType(db.Model):
    __tablename__ = 'property_types'
    type_id = db.Column(db.Integer, primary_key=True)
    type_name = db.Column(db.String(8))


class PropertySource(db.Model):
    __tablename__ = 'property_sources'
    source_id = db.Column(db.Integer, primary_key=True)
    source_name = db.Column(db.String(16))


class Property(db.Model):
    __tablename__ = 'properties'
    property_id = db.Column(db.Integer, primary_key=True)
    city_id = db.Column(db.Integer, db.ForeignKey('cities.city_id'))
    district_id = db.Column(db.Integer, db.ForeignKey('districts.district_id'))
    estate_id = db.Column(db.Integer, db.ForeignKey('estates.estate_id'))
    area_id = db.Column(db.Integer, db.ForeignKey('areas.area_id'))
    build_no = db.Column(db.String(16))
    floor = db.Column(db.Integer)
    floor_all = db.Column(db.Integer)
    room_no = db.Column(db.String(16))
    count_f = db.Column(db.Integer, default=0)  # 室
    count_t = db.Column(db.Integer, default=0)  # 厅
    count_w = db.Column(db.Integer, default=0)  # 卫
    count_y = db.Column(db.Integer, default=0)  # 阳台
    property_type = db.Column(db.Integer)
    property_direction = db.Column(db.String(8))
    square = db.Column(db.Float)
    owner_name = db.Column(db.String(16))
    contact_name = db.Column(db.String(16))
    contact_tel = db.Column(db.String(32))
    status = db.Column(db.Integer, default=0) # 不明，未租，已租
    furniture = db.Column(db.String(64))
    description = db.Column(db.String(256))
    valid_time = db.Column(db.DateTime(), default=datetime.now) # 打电话后确认可租时间，没租掉，则这个时间有用
    trust_grade = db.Column(db.Integer)  # 可信度
    rent_price = db.Column(db.Float)
    mgt_price = db.Column(db.Float)
    reg_user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    reg_time = db.Column(db.DateTime(), default=datetime.now)
    is_deleted = db.Column(db.Boolean, default=False)
    longitude = db.Column(db.String(24))
    latitude = db.Column(db.String(24))
    source = db.Column(db.String(16))

    follows = db.relationship('Follow', backref='property', lazy='dynamic')

    def get_status(self):
        return  ["可租", "已租", "未知"][self.status]

    def get_layout(self):
        return str(self.count_f)+"-"+str(self.count_t)+"-"+str(self.count_w)

    def get_id_str(self):
        return "%06d" % self.property_id


class Follow(db.Model):
    __tablename__ = 'follows'
    follow_id = db.Column(db.Integer, primary_key=True)
    property_id = db.Column(db.Integer, db.ForeignKey('properties.property_id'))
    follow_time = db.Column(db.DateTime(), default=datetime.now)
    follow_user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    follow_content = db.Column(db.String(128))
    alert_time = db.Column(db.DateTime(), default=datetime.now)
    alert_user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    alert_content = db.Column(db.String(128))
    process_time = db.Column(db.DateTime(), default=datetime.now)
    process_user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    process_content = db.Column(db.String(128))


class Image(db.Model):
    __tablename__ = 'images'
    image_id = db.Column(db.Integer, primary_key=True)
    property_id = db.Column(db.Integer, db.ForeignKey('properties.property_id'))
    file_name = db.Column(db.String(32))


class Estate(db.Model):
    __tablename__ = 'estates'
    estate_id = db.Column(db.Integer, primary_key=True)
    estate_name = db.Column(db.String(32))
    city_id = db.Column(db.Integer, db.ForeignKey('cities.city_id'))
    district_id = db.Column(db.Integer, db.ForeignKey('districts.district_id'))
    area_id = db.Column(db.Integer, db.ForeignKey('areas.area_id'))
    english_name = db.Column(db.String(64))
    zhpy         = db.Column(db.String(16))
    complete_year  = db.Column(db.String(8))
    address = db.Column(db.String(64))
    developer = db.Column(db.String(32))
    mgt_company = db.Column(db.String(32))
    mgt_fee  = db.Column(db.Integer)
    total_sqare = db.Column(db.Float)
    total_houses = db.Column(db.Integer)
    floor_area_ratio = db.Column(db.Float)
    parking_no = db.Column(db.Integer)
    green_rate = db.Column(db.Float)
    introduction = db.Column(db.String(256))
    create_time = db.Column(db.DateTime(), default=datetime.now)

    properties = db.relationship('Property', backref='estate', lazy='dynamic')


# Distinct 区县表
# 	DistinctId	区域编号
# 	DistinctName	区域名称
# 	CityId	城市编号
class District(db.Model):
    __tablename__ = 'districts'
    district_id = db.Column(db.Integer, primary_key=True)
    district_name = db.Column(db.String(16))
    city_id = db.Column(db.Integer, db.ForeignKey('cities.city_id'))

    estates = db.relationship('Estate', backref='district', lazy='dynamic')
    properties = db.relationship('Property', backref='district', lazy='dynamic')

# Area 片区表
# 	AreaID	片区编号
# 	AreaName	片区名称
# 	DistinctID	片区所属区域编号, 一个版块可能属于不同的区，因此不用！
# 	CityID	所属城市编号
class Area(db.Model):
    __tablename__ = 'areas'
    area_id = db.Column(db.Integer, primary_key=True)
    area_name = db.Column(db.String(16), unique=True)
    city_id = db.Column(db.Integer, db.ForeignKey('cities.city_id'))

    estates = db.relationship('Estate', backref='area', lazy='dynamic')
    properties = db.relationship('Property', backref='area', lazy='dynamic')

# City 城市表
# 	CityId	城市编号
# 	CityNo	城市区号
# 	CityName	城市名称
class City(db.Model):
    __tablename__ = 'cities'
    city_id = db.Column(db.Integer, primary_key=True)
    city_no = db.Column(db.String(8), unique=True)
    city_name = db.Column(db.String(16), unique=True)

    districts = db.relationship('District', backref='city', lazy='dynamic' )
    areas = db.relationship('Area', backref='city', lazy='dynamic')
    estates = db.relationship('Estate', backref='city', lazy='dynamic')
    properties = db.relationship('Property', backref='city', lazy='dynamic')


