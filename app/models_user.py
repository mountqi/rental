from datetime import datetime, timedelta
import hashlib
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from markdown import markdown
import bleach
from flask import current_app, request, url_for
from flask_login import UserMixin, AnonymousUserMixin
from app.exceptions import ValidationError
from . import db, login_manager
from .models_property import Follow

"""
添加/配置权限组
添加/修改管理账户
数据备份/恢复
添加/删除房源
修改房源信息
更新房源状态
建立/更改用户
房源基本信息访问
房源联系方式访问
房源状态跟进
添加待审核房源
"""

class Permission:
    # 添加/配置权限组
    ADD_MOD_PMSN_GRP = 0x01
    # 添加/修改管理账户
    ADD_MOD_ADMIN_USER = 0x02
    # 数据备份/恢复
    BACKUP_RESTORE_DATA = 0x04
    # 添加/删除房源
    ADD_DEL_HOUSE = 0x08
    # 修改房源信息
    MOD_HOUSE_INFO = 0x10
    # 更新房源状态
    MOD_HOUSE_STATUS = 0x20
    # 建立 / 更改用户
    ADD_MOD_CUSTOMER = 0x40
    # 房源基本信息访问
    VISIT_HOUSE_INFO = 0x80
    # 房源联系方式访问
    VISIT_HOUSE_CONTACT = 0x100
    # 房源状态跟进
    FOLLOW_HOUSE_STATUS = 0x200
    # 添加待审核房源
    PRE_ADD_HOUSE = 0x400

    @staticmethod
    def is_admin_IT(permisson):
        return Permission.BACKUP_RESTORE_DATA & int(permisson) != 0

    @staticmethod
    def is_admin_backend_management(permisson):
        return (Permission.ADD_MOD_PMSN_GRP |
                Permission.ADD_MOD_ADMIN_USER) & int(permisson) != 0

    @staticmethod
    def is_admin_house_management(permisson):
        return (Permission.ADD_DEL_HOUSE |
                Permission.MOD_HOUSE_INFO |
                Permission.MOD_HOUSE_STATUS) & int(permisson) != 0

    @staticmethod
    def is_admin_customer_management(permisson):
        return int(permisson) & Permission.ADD_MOD_CUSTOMER != 0


    @staticmethod
    def is_customer(permisson):
        return (Permission.VISIT_HOUSE_INFO |
                Permission.VISIT_HOUSE_CONTACT |
                Permission.PRE_ADD_HOUSE |
                Permission.FOLLOW_HOUSE_STATUS) & int(permisson) != 0

role_dict = {
    "系统管理" : {
        Permission.ADD_MOD_PMSN_GRP : "添加/配置权限组",
        Permission.ADD_MOD_ADMIN_USER : "添加/修改管理账户",
        Permission.BACKUP_RESTORE_DATA : "数据备份/恢复"
    },
    "房源管理" : {
        Permission.ADD_DEL_HOUSE : "添加/删除房源",
        Permission.MOD_HOUSE_INFO : "修改房源信息",
        Permission.MOD_HOUSE_STATUS : "更新房源状态"
    },
    "用户管理" : {
        Permission.ADD_MOD_CUSTOMER : "建立/更改用户"
    },
    "用户访问" : {
        Permission.VISIT_HOUSE_INFO : "房源基本信息访问",
        Permission.VISIT_HOUSE_CONTACT : "房源联系方式访问",
        Permission.FOLLOW_HOUSE_STATUS : "房源状态跟进",
        Permission.PRE_ADD_HOUSE : "添加待审核房源"
    }
}


class RoleGroup(db.Model):
    __tablename__ = 'role_groups'
    role_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    permissions = db.Column(db.Integer)
    remark = db.Column(db.String(256))
    users = db.relationship('User', backref='role', lazy='dynamic')

    @staticmethod
    def insert_role_group():
        roles = {
            # IT维护组
            'IT维护组': Permission.ADD_MOD_PMSN_GRP |
                          Permission.ADD_MOD_ADMIN_USER |
                          Permission.BACKUP_RESTORE_DATA,

            # 系统管理组
            '系统管理组': Permission.ADD_MOD_PMSN_GRP |
                          Permission.ADD_MOD_ADMIN_USER |
                          Permission.ADD_DEL_HOUSE |
                          Permission.MOD_HOUSE_INFO |
                          Permission.MOD_HOUSE_STATUS |
                          Permission.ADD_MOD_CUSTOMER,

            # 用户管理组
            '用户管理组': Permission.ADD_MOD_CUSTOMER,

            # 房源录入组
            '房源录入组': Permission.ADD_DEL_HOUSE |
                          Permission.MOD_HOUSE_INFO |
                          Permission.MOD_HOUSE_STATUS,

            # 状态更新组
            '状态更新组': Permission.MOD_HOUSE_STATUS,

            # 个人用户组
            '个人用户组': Permission.VISIT_HOUSE_INFO |
                          Permission.VISIT_HOUSE_CONTACT |
                          Permission.FOLLOW_HOUSE_STATUS |
                          Permission.PRE_ADD_HOUSE,

            # 公司用户组
            '公司用户组': Permission.ADD_MOD_CUSTOMER,
        }
        for r in roles:
            role = RoleGroup.query.filter_by(name=r).first()
            if role is None:
                role = RoleGroup(name=r)
            role.permissions = roles[r]
            db.session.add(role)
        db.session.commit()

    def __repr__(self):
        return '<RoleGroup %r>' % self.name

class TimeLengthType:
    DAYS   = 0x01
    MONTHS = 0x02

    @staticmethod
    def get_type_str(type):
        if type == TimeLengthType.DAYS:
            return "天"
        if type == TimeLengthType.MONTHS:
            return "月"


class Fee(db.Model):
    __tablename__ = 'fees'
    fee_id = db.Column(db.Integer, primary_key=True)
    fee_name = db.Column(db.String(32), unique=True)
    amount = db.Column(db.Float)
    discount = db.Column(db.Float)
    time_length = db.Column(db.Integer)
    time_length_type = db.Column(db.Integer)
    tickets_no = db.Column(db.Integer)
    is_active = db.Column(db.Boolean, default=True)
    create_time = db.Column(db.DateTime(), default=datetime.now)

    fee_records = db.relationship('FeeRecord', backref='fee', lazy='dynamic')


class FeeRecord(db.Model):
    __tablename__ = 'fee_records'
    fee_record_id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    collector_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    fee_id = db.Column(db.Integer, db.ForeignKey('fees.fee_id'))
    start_time = db.Column(db.DateTime(), default=datetime.now)
    expire_time = db.Column(db.DateTime(), default=datetime.now)
    charge_time = db.Column(db.DateTime(), default=datetime.now)
    is_valid = db.Column(db.Boolean, default=True) # 缴费是否被撤销了


class UserType:
    BACKEND_ADMIN = 1
    PERSONAL_CUSTOMER = 2
    COPR_CUSTOMER = 3
    CORP_SUB_ACCOUNT = 4


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    login_name = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    name = db.Column(db.String(64))
    phone_no = db.Column(db.String(20))
    email = db.Column(db.String(64))
    id_card_no = db.Column(db.String(20))
    role_id = db.Column(db.Integer, db.ForeignKey('role_groups.role_id'))
    create_time = db.Column(db.DateTime(), default=datetime.now)
    user_type = db.Column(db.Integer)
    is_active = db.Column(db.Boolean,default=True) # 这个只对后台管理员有效吧，前端用户看缴费时段
    agency_id = db.Column(db.Integer, db.ForeignKey('agencies.agency_id'))
    remark = db.Column(db.String(256))

    fee_records = db.relationship('FeeRecord',
                                  backref='customer', lazy='dynamic',
                                  foreign_keys=[FeeRecord.customer_id] )

    follows = db.relationship('Follow', backref='user', lazy='dynamic',
                              foreign_keys=[Follow.follow_user_id])

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        # 可能要加上role的判断

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def can(self, permissions):
        return self.role is not None and \
            (self.role.permissions & permissions) == permissions

    def get_id(self):
        return self.user_id

    def is_valid(self):
        # 1. 对于后台管理员，is_active=True表明有效
        if self.user_type == UserType.BACKEND_ADMIN:
            return self.is_active

        # 2. 对于中介公司的子账户，其父账户在付费期内，则是有效的
        if self.user_type == UserType.CORP_SUB_ACCOUNT:
            parent = self.agency.connected_users.filter_by(user_type=UserType.COPR_CUSTOMER).one()
            valid_fee_records = parent.fee_records.filter_by(is_valid=True) \
                .order_by(FeeRecord.expire_time.desc()).all()
        else:
            # 3. 对于中介公司账号和个人用户账号，当前时间在付费期内，则是有效的
            valid_fee_records = self.fee_records.filter_by(is_valid=True) \
                .order_by(FeeRecord.expire_time.desc()).all()

        # 检查付费期
        now = datetime.now()
        for record in valid_fee_records:
            if record.start_time <= now and record.expire_time >= now:
                return True
        return False

            # 下面这个实现不成功，以后再访
            # valid_fee_records = customer.fee_records.\
            #     filter_by(FeeRecord.expire_time>=now).\
            #     filter_by(FeeRecord.start_time<=now).all()
            # return len(valid_fee_records)>0


    def get_active_state_str(self):
        if self.is_valid():
            return "有效"
        else:
            return "无效"

    def is_backend_admin(self):
        return self.user_type == UserType.BACKEND_ADMIN

    def __repr__(self):
        return '<User %r>' % self.login_name


class Agency(db.Model):
    __tablename__ = 'agencies'
    agency_id = db.Column(db.Integer, primary_key=True)
    corp_name = db.Column(db.String(64), unique=True)
    corp_license_no = db.Column(db.String(64))
    create_time = db.Column(db.DateTime(), default=datetime.now)
    sub_account_no = db.Column(db.Integer)

    connected_users = db.relationship('User', backref='agency', lazy='dynamic')


class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False


login_manager.anonymous_user = AnonymousUser


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

