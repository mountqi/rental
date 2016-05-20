"""
城市
区县
片区
楼盘/小区
房源
"""
from flask import render_template, redirect, request, url_for, flash, jsonify, g
from flask_login import login_user, logout_user, login_required, \
    current_user
from sqlalchemy.exc import IntegrityError

from . import admin
from .forms_property import AddCityForm, AddDistrictForm, ShowCityListForDistrictForm, \
    AddAreaForm, ShowCityListForAreaForm, ShowCityListForAdminEstateForm,\
    ShowDistrictListForAdminEstateForm, ShowAreaListForAdminEstateForm, \
    AddModEstateForm, ShowCityListForAdminPropertyForm, ShowDistrictListForAdminPropertyForm,\
    ShowAreaListForAdminPropertyForm, ShowSourceListForAdminPropertyForm,\
    ShowEstateListForAdminPropertyForm, AddPropertyForm, AddFollowForm

from .. import db, check_empty
from ..models_property import City, District, Area, Estate, Property, Follow
from .menu_factory import get_nav_menu, get_tab_menu
from ..decorators import permission_required


@admin.route('/admin/cities',methods=['GET'])
@login_required
# @permission_required(Permission.ADD_MOD_CUSTOMER)
def cities():
    """浏览城市列表
    """
    all_cities = City.query.all()
    return render_template('admin/cities.html',
                           all_cities=all_cities, pagination=None,
                           title="查看城市列表", nav_menu=get_nav_menu(current_user),
                           tab_menu=get_tab_menu("houses", current_user, "城市"))


@admin.route('/admin/add-city',methods=['GET', 'POST'])
@login_required
# @permission_required(Permission.ADD_MOD_ADMIN_USER)
def add_city():
    """添加城市
    """
    form = AddCityForm()
    if form.validate_on_submit():
        city = City()
        city.city_name = form.city_name.data
        city.city_no   = form.city_no.data
        db.session.add(city)
        try:
            db.session.commit()
            flash('城市已经添加')
            return redirect(url_for('admin.cities'))
        except IntegrityError as error:
            db.session.rollback()
            flash('城市已经存在，添加失败', "error")

    return render_template("admin/common.html", form=form,
                           title="添加城市", nav_menu=get_nav_menu(current_user),
                           tab_menu=get_tab_menu("houses", current_user, "城市"))


@admin.route('/admin/districts',methods=['GET'])
@login_required
# @permission_required(Permission.ADD_MOD_CUSTOMER)
def districts():
    """浏览某个城市的区县
    """
    city_id = request.args.get('city_id', 0, type=int)
    if city_id==0:
        city_id = 1

    city_form = ShowCityListForDistrictForm( city_id=city_id )
    city = City.query.filter_by(city_id=city_id).first()
    all_districts = District.query.filter_by(city_id=city_id).all()
    return render_template('admin/districts.html',
                           all_districts=all_districts, pagination=None,
                           title="查看区县列表", nav_menu=get_nav_menu(current_user),
                           tab_menu=get_tab_menu("houses", current_user, "区县"),
                           city_id=city_id, city=city, city_form=city_form)


@admin.route('/admin/add-district/<int:city_id>',methods=['GET', 'POST'])
@login_required
# @permission_required(Permission.ADD_MOD_ADMIN_USER)
def add_district(city_id):
    """添加区县
    """
    form = AddDistrictForm()
    if form.validate_on_submit():
        district = District()
        district.district_name = form.district_name.data
        district.city_id = city_id
        db.session.add(district)
        try:
            db.session.commit()
            flash('区县已经添加')
            return redirect(url_for('admin.districts', city_id=city_id))
        except IntegrityError as error:
            db.session.rollback()
            flash('区县已经存在，添加失败', "error")

    return render_template("admin/common.html", form=form,
                           title="添加区县", nav_menu=get_nav_menu(current_user),
                           tab_menu=get_tab_menu("houses", current_user, "区县"))


@admin.route('/admin/areas',methods=['GET'])
@login_required
# @permission_required(Permission.ADD_MOD_CUSTOMER)
def areas():
    """浏览某个城市的房源区域
    """
    city_id = request.args.get('city_id', 0, type=int)
    if city_id==0:
        city_id = 1

    city_form = ShowCityListForAreaForm( city_id=city_id )
    city = City.query.filter_by(city_id=city_id).first()
    all_areas = Area.query.filter_by(city_id=city_id).all()
    return render_template('admin/areas.html',
                           all_areas=all_areas, pagination=None,
                           title="查看区域列表", nav_menu=get_nav_menu(current_user),
                           tab_menu=get_tab_menu("houses", current_user, "区域"),
                           city_id=city_id, city=city, city_form=city_form)


@admin.route('/admin/add-area/<int:city_id>',methods=['GET', 'POST'])
@login_required
# @permission_required(Permission.ADD_MOD_ADMIN_USER)
def add_area(city_id):
    """添加房源区域
    """
    form = AddAreaForm()
    if form.validate_on_submit():
        area = Area()
        area.area_name = form.area_name.data
        area.city_id = city_id
        db.session.add(area)
        try:
            db.session.commit()
            flash('区域已经添加')
            return redirect(url_for('admin.areas', city_id=city_id))
        except IntegrityError as error:
            db.session.rollback()
            flash('区域已经存在，添加失败', "error")

    return render_template("admin/common.html", form=form,
                           title="添加区域", nav_menu=get_nav_menu(current_user),
                           tab_menu=get_tab_menu("houses", current_user, "区域"))


@admin.route('/admin/estates',methods=['GET'])
@login_required
# @permission_required(Permission.ADD_MOD_CUSTOMER)
def estates():
    """浏览楼盘
    """
    g.city_id = request.args.get('city_id', 0, type=int)
    if g.city_id==0:
        g.city_id = 1

    g.district_id = request.args.get('district_id', 0, type=int)
    g.area_id = request.args.get('area_id', 0, type=int)

    form_param = {}
    form_param['city_id'] = g.city_id
    form_param['district_id'] = g.district_id
    form_param['area_id'] = g.area_id

    g.city_form = ShowCityListForAdminEstateForm( **form_param )
    g.district_form = ShowDistrictListForAdminEstateForm(**form_param )
    g.area_form = ShowAreaListForAdminEstateForm(**form_param )
    g.nav_menu = get_nav_menu(current_user)
    g.tab_menu=get_tab_menu("houses", current_user, "楼盘")
    g.pagination=None
    g.all_estates=None

    estate_query = Estate.query.filter_by( city_id=g.city_id )
    if g.district_id!=0:
        estate_query = estate_query.filter_by( district_id=g.district_id )
    if g.area_id != 0:
        estate_query = estate_query.filter_by(area_id=g.area_id)

    page = request.args.get('page', 1, type=int)
    pagination = estate_query.paginate( page, per_page=10, error_out=False)
    g.all_estates = pagination.items

    return render_template('admin/estates.html', title="查看楼盘/小区列表",
                           nav_menu=g.nav_menu, tab_menu=g.tab_menu,pagination=pagination )


@admin.route('/admin/add-estate/<int:city_id>/<int:district_id>/<int:area_id>',methods=['GET', 'POST'])
@login_required
# @permission_required(Permission.ADD_MOD_ADMIN_USER)
def add_estate(city_id,district_id,area_id):
    """添加楼盘
    """

    form = AddModEstateForm(city_id=city_id)
    if request.method == "GET":
        form.district.data = district_id
        form.area.data = area_id

    if form.validate_on_submit():
        estate = Estate()
        estate.estate_name = form.estate_name.data
        estate.city_id = city_id
        estate.district_id = form.district.data
        estate.area_id = form.area.data
        estate.english_name = form.english_name.data
        estate.zhpy = form.zhpy.data
        estate.complete_year = form.complete_year.data
        estate.address = form.address.data
        estate.developer = form.developer.data
        estate.mgt_company = form.mgt_company.data
        estate.mgt_fee = form.mgt_fee.data
        estate.total_sqare = form.total_sqare.data
        estate.total_houses = form.total_houses.data
        estate.floor_area_ratio = form.floor_area_ratio.data
        estate.parking_no = form.parking_no.data
        estate.green_rate = form.green_rate.data
        estate.introduction = form.introduction.data
        db.session.add(estate)
        try:
            db.session.commit()
            flash('楼盘/小区已经添加')
            return redirect(url_for('admin.add_estate', city_id=city_id, district_id=form.district.data,
                                    area_id=form.area.data))
        except IntegrityError as error:
            db.session.rollback()
            flash('楼盘/小区已经存在，添加失败', "error")

    return render_template("admin/add_estate.html", form=form,
                           title="添加楼盘/小区", nav_menu=get_nav_menu(current_user),
                           tab_menu=get_tab_menu("houses", current_user, "楼盘"))


@admin.route('/admin/mod-estate/<int:city_id>/<int:estate_id>',methods=['GET', 'POST'])
@login_required
# @permission_required(Permission.ADD_MOD_ADMIN_USER)
def mod_estate(city_id,estate_id):
    """修改楼盘
    """
    g.city_id = city_id
    g.estate_id = estate_id
    form = AddModEstateForm(city_id=city_id)
    estate = Estate.query.filter_by(estate_id=estate_id).one()

    if form.validate_on_submit():
        estate = Estate()
        estate.estate_name = form.estate_name.data
        estate.city_id = city_id
        estate.district_id = form.district.data
        estate.area_id = form.area.data
        estate.english_name = form.english_name.data
        estate.zhpy = form.zhpy.data
        estate.complete_year = form.complete_year.data
        estate.address = form.address.data
        estate.developer = form.developer.data
        estate.mgt_company = form.mgt_company.data
        estate.mgt_fee = form.mgt_fee.data
        estate.total_sqare = form.total_sqare.data
        estate.total_houses = form.total_houses.data
        estate.floor_area_ratio = form.floor_area_ratio.data
        estate.parking_no = form.parking_no.data
        estate.green_rate = form.green_rate.data
        estate.introduction = form.introduction.data
        db.session.add(estate)
        try:
            db.session.commit()
            flash('楼盘/小区已经修改')
            return redirect(url_for('admin.add_estate', city_id=city_id, district_id=form.district.data,
                                    area_id=form.area.data))
        except IntegrityError as error:
            db.session.rollback()
            flash('楼盘/小区修改失败', "error")

    if request.method == "GET":
        form.estate_name.data = estate.estate_name
        form.district.data = estate.district_id
        form.area.data = estate.area_id
        form.english_name.data = estate.english_name
        form.zhpy.data = estate.zhpy
        form.complete_year.data = estate.complete_year
        form.address.data = estate.address
        form.developer.data = estate.developer
        form.mgt_company.data = estate.mgt_company
        form.mgt_fee.data = estate.mgt_fee
        form.total_sqare.data = estate.total_sqare
        form.total_houses.data = estate.total_houses
        form.floor_area_ratio.data = estate.floor_area_ratio
        form.parking_no.data = estate.parking_no
        form.green_rate.data = estate.green_rate
        form.introduction.data = estate.introduction

    return render_template("admin/add_estate.html", form=form,
                           title="修改楼盘/小区", nav_menu=get_nav_menu(current_user),
                           tab_menu=get_tab_menu("houses", current_user, "楼盘"))


@admin.route('/admin/properties',methods=['GET'])
@login_required
# @permission_required(Permission.ADD_MOD_CUSTOMER)
def properties():
    """浏览房源
    """
    g.city_id = request.args.get('city_id', 0, type=int)
    if g.city_id == 0:
        g.city_id = 1

    g.district_id = request.args.get('district_id', 0, type=int)
    g.estate_id = request.args.get('estate_id', 0, type=int)
    g.area_id = request.args.get('area_id', 0, type=int)
    g.source = request.args.get('source', "", type=str)
    form_param = {}
    form_param['city_id'] = g.city_id
    form_param['estate_id'] = g.estate_id
    form_param['district_id'] = g.district_id
    form_param['area_id'] = g.area_id
    form_param['source'] = g.source
    form_param['url'] = "admin.properties"
    g.city_form = ShowCityListForAdminPropertyForm(**form_param)
    g.district_form = ShowDistrictListForAdminPropertyForm(**form_param)
    g.estate_form = ShowEstateListForAdminPropertyForm(**form_param)
    g.area_form = ShowAreaListForAdminPropertyForm(**form_param)
    g.source_form = ShowSourceListForAdminPropertyForm(**form_param)

    g.nav_menu = get_nav_menu(current_user)
    g.tab_menu = get_tab_menu("houses", current_user, "房源")
    g.pagination = None
    g.all_properties = None

    property_query = Property.query
    if g.estate_id != 0:
        property_query = property_query.filter_by(estate_id=g.estate_id)
    elif g.district_id != 0:
        property_query = property_query.filter_by(district_id=g.district_id)
    else :
        property_query = property_query.filter_by(city_id=g.city_id)
        if g.area_id != 0:
            property_query = property_query.filter_by(area_id=g.area_id)

    if g.source !="":
        property_query = property_query.filter_by(source=g.source)

    page = request.args.get('page', 1, type=int)
    pagination = property_query.paginate(page, per_page=10, error_out=False)
    g.all_properties = pagination.items

    return render_template('admin/properties.html', title="浏览房源",
                           nav_menu=g.nav_menu, tab_menu=g.tab_menu, pagination=pagination,
                           prev_url = request.url )


@admin.route('/admin/district-list')
@login_required
def district_list():
    """根据city，给出下属区县列表
    """
    city_id = request.args.get('city_id', 0, type=int)
    districts = [(district.district_id, district.district_name)
                             for district in District.query.filter_by(city_id=city_id).all()]

    return jsonify({
        'districts' : districts
    })


@admin.route('/admin/estate-list')
@login_required
def estate_list():
    """根据district，给出楼盘列表
    """
    district_id = request.args.get('district_id', 0, type=int)
    estates = [(estate.estate_id, estate.estate_name)
                             for estate in Estate.query.filter_by(district_id=district_id).all()]

    return jsonify({
        'estates' : estates
    })


@admin.route('/admin/area-list')
@login_required
def area_list():
    """根据city，给出下属房源区域列表
    """
    city_id = request.args.get('city_id', 0, type=int)
    areas = [(area.area_id, area.area_name)
                             for area in Area.query.filter_by(city_id=city_id).all()]

    return jsonify({
        'areas' : areas
    })


@admin.route('/admin/add-property',methods=['GET', 'POST'])
@login_required
# @permission_required(Permission.ADD_MOD_ADMIN_USER)
def add_property():
    """添加房源
    """
    g.city_id = request.args.get('city_id', 0, type=int)
    if g.city_id == 0:
        g.city_id = 1

    g.district_id = request.args.get('district_id', 0, type=int)
    g.estate_id = request.args.get('estate_id', 0, type=int)
    g.area_id = request.args.get('area_id', 0, type=int)
    g.source = request.args.get('source', "", type=str)
    form_param = {}
    form_param['city_id'] = g.city_id
    form_param['estate_id'] = g.estate_id
    form_param['district_id'] = g.district_id
    form_param['area_id'] = g.area_id
    form_param['source'] = g.source

    form = AddPropertyForm(**form_param)
    if request.method == "GET":
        form.city.data = g.city_id
        form.district.data = g.district_id
        form.estate.data = g.estate_id
        form.area.data = g.area_id
    elif request.method == "POST":
        form_param['city_id'] = form.city.data
        form_param['district_id'] = form.district.data
        form_param['estate_id'] = form.estate.data
        form_param['area_id'] = form.area.data
        form = AddPropertyForm(**form_param)

    if form.validate_on_submit():
        property = Property()
        property.city_id = form.city.data
        property.district_id = form.district.data
        property.estate_id = form.estate.data
        property.area_id = form.area.data
        property.build_no = form.build_no.data
        property.floor = form.floor.data
        property.floor_all = form.floor_all.data
        property.room_no = form.room_no.data
        property.count_f = form.count_f.data
        property.count_t = form.count_t.data
        property.count_w = form.count_w.data
        property.count_y = form.count_y.data
        property.property_type = form.property_type.data
        property.property_direction = form.property_direction.data
        property.square = form.square.data
        property.owner_name = form.owner_name.data
        property.contact_name = form.contact_name.data
        property.contact_tel = form.contact_tel.data
        property.status = form.status.data
        property.furniture = form.furniture.data
        property.description = form.description.data
        property.valid_time = form.valid_time.data
        property.trust_grade = form.trust_grade.data
        property.rent_price = form.rent_price.data
        property.mgt_price = form.mgt_price.data
        property.reg_user_id = current_user.user_id
        property.longitude = form.longitude.data
        property.latitude = form.latitude.data
        property.source = form.source.data

        db.session.add(property)
        try:
            db.session.commit()
            flash('房源已经添加')
            return redirect(url_for('admin.add_property', **form_param))
        except IntegrityError as error:
            db.session.rollback()
            flash('房源已经存在，添加失败', "error")

    return render_template("admin/add_property.html", form=form,
                           title="添加房源", nav_menu=get_nav_menu(current_user),
                           tab_menu=get_tab_menu("houses", current_user, "房源"))


@admin.route('/admin/mod-property/<int:property_id>',methods=['GET', 'POST'])
@login_required
# @permission_required(Permission.ADD_MOD_ADMIN_USER)
def mod_property(property_id):
    """修改房源信息
    """
    g.city_id = request.args.get('city_id', 0, type=int)
    if g.city_id == 0:
        g.city_id = 1

    g.district_id = request.args.get('district_id', 0, type=int)
    g.estate_id = request.args.get('estate_id', 0, type=int)
    g.area_id = request.args.get('area_id', 0, type=int)
    g.source = request.args.get('source', "", type=str)
    next_url = request.args.get('next', url_for("admin.properties"), type=str)

    form_param = {}
    form_param['city_id'] = g.city_id
    form_param['estate_id'] = g.estate_id
    form_param['district_id'] = g.district_id
    form_param['area_id'] = g.area_id
    form_param['source'] = g.source

    property = Property.query.filter_by(property_id=property_id).one()

    form = AddPropertyForm(**form_param)
    if request.method == "GET":
        form.city.data = g.city_id
        form.district.data = g.district_id
        form.estate.data = g.estate_id
        form.area.data = g.area_id
    elif request.method == "POST":
        form_param['city_id'] = form.city.data
        form_param['district_id'] = form.district.data
        form_param['estate_id'] = form.estate.data
        form_param['area_id'] = form.area.data
        form = AddPropertyForm(**form_param)

    if form.validate_on_submit():
        property.city_id = form.city.data
        property.district_id = form.district.data
        property.estate_id = form.estate.data
        property.area_id = form.area.data
        property.build_no = form.build_no.data
        property.floor = form.floor.data
        property.floor_all = form.floor_all.data
        property.room_no = form.room_no.data
        property.count_f = form.count_f.data
        property.count_t = form.count_t.data
        property.count_w = form.count_w.data
        property.count_y = form.count_y.data
        property.property_type = form.property_type.data
        property.property_direction = form.property_direction.data
        property.square = form.square.data
        property.owner_name = form.owner_name.data
        property.contact_name = form.contact_name.data
        property.contact_tel = form.contact_tel.data
        property.status = form.status.data
        property.furniture = form.furniture.data
        property.description = form.description.data
        property.valid_time = form.valid_time.data
        property.trust_grade = form.trust_grade.data
        property.rent_price = form.rent_price.data
        property.mgt_price = form.mgt_price.data
        property.reg_user_id = current_user.user_id
        property.longitude = form.longitude.data
        property.latitude = form.latitude.data
        property.source = form.source.data

        db.session.add(property)
        try:
            db.session.commit()
            flash('房源修改完毕')
            # return redirect(url_for('admin.add_property', **form_param))
            return redirect(next_url)
        except IntegrityError as error:
            db.session.rollback()
            flash('房源修改失败', "error")

    if request.method == "GET":
        form.city.data = property.city_id
        form.district.data = property.district_id
        form.estate.data = property.estate_id
        form.area.data = property.area_id
        form.build_no.data = property.build_no
        form.floor.data = property.floor
        form.floor_all.data = property.floor_all
        form.room_no.data = property.room_no
        form.count_f.data = property.count_f
        form.count_t.data = property.count_t
        form.count_w.data = property.count_w
        form.count_y.data = property.count_y
        form.property_type.data = property.property_type
        form.property_direction.data = property.property_direction
        form.square.data = property.square
        form.owner_name.data = property.square
        form.contact_name.data = property.contact_name
        form.contact_tel.data = property.contact_tel
        form.status.data = property.status
        form.furniture.data = property.furniture
        form.description.data = property.description
        form.valid_time.data = property.valid_time
        form.trust_grade.data = property.trust_grade
        form.rent_price.data = property.rent_price
        form.mgt_price.data = property.mgt_price
        form.longitude.data = property.longitude
        form.latitude.data = property.latitude
        form.source.data = property.source

    return render_template("admin/mod_property.html", form=form,
                           title="修改房源信息", nav_menu=get_nav_menu(current_user),
                           tab_menu=get_tab_menu("houses", current_user, "房源"))


@admin.route('/admin/batch-mod-property',methods=['GET', 'POST'])
@login_required
# @permission_required(Permission.ADD_MOD_ADMIN_USER)
def batch_mod_property():
    """批量修改房源信息，一个一个的修改
    """
    return render_template("admin/batch_mod_property.html",
                           title="批量修改房源信息", nav_menu=get_nav_menu(current_user),
                           tab_menu=get_tab_menu("houses", current_user, "房源"))


@admin.route('/admin/follow-property/<int:property_id>',methods=['GET', 'POST'])
@login_required
# @permission_required(Permission.ADD_MOD_ADMIN_USER)
def follow_property(property_id):
    """跟进房源状态
    """
    next_url = request.args.get('next', url_for("admin.properties"), type=str)
    form = AddFollowForm()
    if form.validate_on_submit():
        follow = Follow()
        follow.follow_content = form.follow_content.data
        follow.property_id = property_id
        follow.follow_user_id = current_user.user_id
        db.session.add(follow)
        try:
            db.session.commit()
            flash('房源跟进已经添加')
            return redirect(next_url)
        except IntegrityError as error:
            db.session.rollback()
            flash('房源跟进添加失败', "error")

    g.property = Property.query.filter_by(property_id=property_id).one()
    g.follows = Follow.query.filter_by(property_id=property_id).all()
    return render_template("admin/follow.html", form=form,
                           title="添加城市", nav_menu=get_nav_menu(current_user),
                           tab_menu=get_tab_menu("houses", current_user, "城市"))

