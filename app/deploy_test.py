import datetime
from . import db, login_manager
from .user_models import User, RoleGroup, UserType, Agency, Fee, FeeRecord, TimeLengthType

def deploy_test():
    RoleGroup.insert_role_group()

    if not User.query.filter_by(login_name="superadmin").first():
        user = User(login_name="superadmin")
        user.password = "test"
        user.role = RoleGroup.query.filter_by(name="系统管理组").first()
        user.user_type = UserType.BACKEND_ADMIN
        db.session.add(user)
        db.session.commit()

    if not User.query.filter_by(login_name="it").first():
        user = User(login_name="it")
        user.password = "test"
        user.role = RoleGroup.query.filter_by(name="IT维护组").first()
        user.user_type = UserType.BACKEND_ADMIN
        db.session.add(user)
        db.session.commit()

    customeradmin = User.query.filter_by(login_name="customeradmin").first()
    if not customeradmin:
        customeradmin = User(login_name="customeradmin")
        customeradmin.password = "test"
        customeradmin.role = RoleGroup.query.filter_by(name="用户管理组").first()
        customeradmin.user_type = UserType.BACKEND_ADMIN
        db.session.add(customeradmin)
        db.session.commit()

    if not User.query.filter_by(login_name="housemanager").first():
        user = User(login_name="housemanager")
        user.password = "test"
        user.role = RoleGroup.query.filter_by(name="房源录入组").first()
        user.user_type = UserType.BACKEND_ADMIN
        db.session.add(user)
        db.session.commit()

    if not User.query.filter_by(login_name="houseupdate").first():
        user = User(login_name="houseupdate")
        user.password = "test"
        user.role = RoleGroup.query.filter_by(name="状态更新组").first()
        user.user_type = UserType.BACKEND_ADMIN
        db.session.add(user)
        db.session.commit()

    personalcustomer = User.query.filter_by(login_name="personalcustomer").first()
    if not personalcustomer:
        personalcustomer = User(login_name="personalcustomer")
        personalcustomer.password = "test"
        personalcustomer.role = RoleGroup.query.filter_by(name="个人用户组").first()
        personalcustomer.user_type = UserType.PERSONAL_CUSTOMER
        db.session.add(personalcustomer)
        db.session.commit()

    agency = Agency.query.filter_by(corp_name="链家中介").first()
    if not agency:
        agency = Agency(corp_name="链家中介")
        agency.corp_license_no = "124215235234562"
        agency.sub_account_no = 3
        db.session.add(agency)
        db.session.commit()

    if not User.query.filter_by(login_name="corpcustomer").first():
        user = User(login_name="corpcustomer")
        user.password = "test"
        user.role = RoleGroup.query.filter_by(name="公司用户组").first()
        user.user_type = UserType.COPR_CUSTOMER
        user.agency_id = agency.agency_id
        db.session.add(user)
        db.session.commit()

    if not User.query.filter_by(login_name="13353235824").first():
        user = User(login_name="13353235824")
        user.password = "test"
        user.role = RoleGroup.query.filter_by(name="个人用户组").first()
        user.user_type = UserType.CORP_SUB_ACCOUNT
        user.agency_id = agency.agency_id
        user.name = "张三"
        db.session.add(user)
        db.session.commit()

    if not User.query.filter_by(login_name="13953235855").first():
        user = User(login_name="13953235855")
        user.password = "test"
        user.role = RoleGroup.query.filter_by(name="个人用户组").first()
        user.user_type = UserType.CORP_SUB_ACCOUNT
        user.agency_id = agency.agency_id
        user.name = "李四"
        db.session.add(user)
        db.session.commit()

    # 添加收费
    fee = Fee.query.filter_by(fee_name="月付1500").first()
    if not fee:
        fee = Fee(fee_name="月付1500")
        fee.amount = 1500
        fee.discount = 1.0
        fee.tickets_no = 30
        fee.time_length = 1
        fee.time_length_type = TimeLengthType.MONTHS
        db.session.add(fee)
        db.session.commit()


    feeDays = Fee.query.filter_by(fee_name="周付400").first()
    if not feeDays:
        feeDays = Fee(fee_name="周付400")
        feeDays.amount = 400
        feeDays.discount = 1.0
        feeDays.tickets_no = 30
        feeDays.time_length = 7
        feeDays.time_length_type = TimeLengthType.DAYS
        db.session.add(feeDays)
        db.session.commit()

    fee_record = FeeRecord()
    fee_record.collector_id = customeradmin.user_id
    fee_record.customer_id = personalcustomer.user_id
    fee_record.fee_id = fee.fee_id
    fee_record.start_time = datetime.datetime.now()
    fee_record.expire_time = fee_record.start_time + datetime.timedelta(days=31)
    db.session.add(fee_record)
    personalcustomer.expire_time = fee_record.expire_time
    db.session.add(personalcustomer)
    db.session.commit()