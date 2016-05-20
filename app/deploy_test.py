import datetime
from . import db, login_manager
from .models_user import User, RoleGroup, UserType, Agency, Fee, FeeRecord, TimeLengthType
from .models_property import City, District, Area, Estate, Property, PropertySource, PropertyType

def add_house_data():
    # Add city
    if not City.query.filter_by(city_name="上海").first():
        city = City(city_name="上海")
        city.city_no = "021"
        db.session.add(city)
        db.session.commit()

    # Add District
    district_list = ["黄浦区",
                     "卢湾区",
                     "徐汇区",
                     "长宁区",
                     "静安区",
                     "普陀区",
                     "闸北区",
                     "虹口区",
                     "杨浦区",
                     "宝山区",
                     "闵行区",
                     "嘉定区",
                     "浦东新区",
                     "松江区",
                     "金山区",
                     "青浦区",
                     "南汇区",
                     "奉贤区",
                     "崇明县"]
    for name in district_list:
        if not District.query.filter_by(district_name=name).first():
            district = District(district_name=name)
            district.city_id = city.city_id
            db.session.add(district)
            db.session.commit()

    # Add estate
    estates_list = [
        ('金俊苑', '虹井路368弄',  '小高层', '2000'),
        ('西郊宝城花苑', '金滨路101弄','别墅', '2003'),
        ('龙柏山庄', '虹桥路2489弄188号','别墅', '2004'),
        ('荣轩大厦', '镇宁路233号', '高层', '2001'),
        ('四季晶园', '水城南路16弄', '高层', '2001'),
        ('翠庭(虹桥)', '紫云西路28弄','高层', '2002') ]
    district = District.query.filter_by(district_name='长宁区').first()

    for estate in estates_list:
        if not Estate.query.filter_by(estate_name=estate[0]).first():
            new_estate = Estate(estate_name=estate[0])
            new_estate.city_id = city.city_id
            new_estate.district_id = district.district_id
            new_estate.address = estate[1]
            new_estate.property_type = estate[2]
            new_estate.complete_year = estate[3]
            db.session.add(new_estate)
            db.session.commit()

    # Add area
    area_list = ["古北",
                     "虹桥",
                     "中山公园",
                     "徐家汇"]
    for name in area_list:
        if not Area.query.filter_by(area_name=name).first():
            area = Area(area_name=name)
            area.city_id = city.city_id
            db.session.add(area)
            db.session.commit()

    # Add properties
    properties_list = [
        (1, 4, 1, 1, "18号楼", 8, 19, "203室", 3, 2, 1, 1, 120, "张三", "", "12923423", "M 源涞国际", 8000, "住宅公寓"),
        (1, 4, 1, 2, "19号楼", 3, 19, "303室", 2, 2, 1, 1, 100, "李四", "", "12923423", "M 源涞国际", 5000, "商住公寓"),
        (1, 4, 1, 2, "12号楼", 2, 19, "103室", 1, 2, 1, 1, 111, "王五", "", "12923423", "L 个人业主", 12000, "老洋房"),
        (1, 4, 1, 2, "13号楼", 5, 19, "203室", 4, 2, 1, 1, 130, "赵六", "", "12923423", "S 比利华" , 20000, "花园洋房")]

    for p in properties_list:
        house = Property()
        house.city_id = p[0]
        house.district_id = p[1]
        house.area_id = p[2]
        house.estate_id = p[3]
        house.build_no = p[4]
        house.floor = p[5]
        house.floor_all = p[6]
        house.room_no = p[7]
        house.status = 0
        house.count_f = p[8]
        house.count_t = p[9]
        house.count_w = p[10]
        house.count_y = p[11]
        house.square = p[12]
        house.owner_name = p[13]
        house.contact_name = p[14]
        house.contact_tel = p[15]
        house.source = p[16]
        house.rent_price = p[17]
        house.property_type = p[18]
        db.session.add(house)
        db.session.commit()

    # Add property source
    source_list = [
        "L 个人业主",
        "M 源涞国际",
        "S 比利华"]

    for source in source_list:
        if not PropertySource.query.filter_by(source_name=name).first():
            s = PropertySource(source_name=source)
            db.session.add(s)
            db.session.commit()


    # Add property type
    type_list = [
                    "独栋别墅",
                    "联排别墅",
                    "住宅公寓",
                    "商住公寓",
                    "老洋房",
                    "老公寓",
                    "花园洋房",
                    "服务式公寓",
                    "酒店式公寓",
                    ]

    for type in type_list:
        if not PropertyType.query.filter_by(type_name=type).first():
            t = PropertyType(type_name=type)
            db.session.add(t)
            db.session.commit()


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

    personalcustomer = User.query.filter_by(login_name="13916608435").first()
    if not personalcustomer:
        personalcustomer = User(login_name="13916608435")
        personalcustomer.name = "张小奇"
        personalcustomer.phone_no = "13916608435"
        personalcustomer.password = "testtest"
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

    add_house_data()