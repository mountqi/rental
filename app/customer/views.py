from flask import render_template, redirect, request, url_for, flash, g
from flask_login import login_user, logout_user, login_required, \
    current_user

from . import customer
from .. import db
from .menu_factory import get_pop_menu, get_nav_menu, get_nav_menu1

from ..models_property import City, District, Area, Estate, Property, Follow, PropertyGrade

from .forms import ShowDistrictListForCustomerProperyForm, ShowAreaListForCustomerProperyForm, \
    ShowEstateListForCustomerPropertyForm, ShowPropertyLayoutForCustomerPropertyForm, \
    ShowSubwayListForCustomerPropertyForm, ShowOwnerTypeListForCustomerPropertyForm, \
    ShowPriceListForCustomerPropertyForm, ShowSquareListForCustomerPropertyForm

from .forms import propery_layouts, square_list, price_list

def process_search():
    g.key = request.args.get('key', '')


def get_sort_icon(id):
    if id==g.sort_by:
        if g.sort_order=='true':
            return '&#xe74d;'
        else:
            return '&#xe7fe;'
    else:
        return '&#xe637;'

def get_sort_attr(id):
    if id == g.sort_by:
        if g.sort_order=='true':
            return 'sort="1" order="true"'
        else:
            return 'sort="1" order="false"'
    else:
        return ''


def set_order_by( property_query ):
    if g.sort_by == "status":
        if g.sort_order == 'true':
            property_query = property_query.order_by(Property.status)
        else:
            property_query = property_query.order_by(Property.status.desc())
    elif g.sort_by == "freshment":
        pass
    elif g.sort_by == "click-count":
        pass
    elif g.sort_by == "estate":
        # 这里很勉强
        if g.sort_order == 'true':
            property_query = property_query.order_by(Property.estate_id)
        else:
            property_query = property_query.order_by(Property.estate_id.desc())
    elif g.sort_by == "prop-layout":
        # 这里很勉强
        if g.sort_order == 'true':
            property_query = property_query.order_by(Property.count_f)
        else:
            property_query = property_query.order_by(Property.count_f.desc())

    elif g.sort_by == "rent-price":
        if g.sort_order == 'true':
            property_query = property_query.order_by(Property.rent_price)
        else:
            property_query = property_query.order_by(Property.rent_price.desc())

    elif g.sort_by == "prop-type":
        if g.sort_order == 'true':
            property_query = property_query.order_by(Property.property_type)
        else:
            property_query = property_query.order_by(Property.property_type.desc())
    elif g.sort_by == "prop-update-date":
        pass
    elif g.sort_by == "prop-no":
        if g.sort_order == 'true':
            property_query = property_query.order_by(Property.property_id)
        else:
            property_query = property_query.order_by(Property.property_id.desc())
    elif g.sort_by == "prop-source":
        if g.sort_order == 'true':
            property_query = property_query.order_by(Property.source_id)
        else:
            property_query = property_query.order_by(Property.source_id.desc())

    return property_query


def process_filter():
    g.city_id = 1
    g.district_id = request.args.get('district_id', 0, type=int)
    g.estate_id = request.args.get('estate_id', 0, type=int)
    g.area_id = request.args.get('area_id', 0, type=int)
    g.layout = request.args.get('layout', 0, type=int)
    g.subway = request.args.get('subway', '')
    g.price = request.args.get('price', 0, type=int)
    g.owner_type = request.args.get('owner_type', 0, type=int)
    g.square = request.args.get('square', 0, type=int)
    g.grade = request.args.get('grade', 0, type=int)
    g.sort_by = request.args.get('sort_by', 'no')
    g.sort_order = request.args.get('sort_order', 'true')
    g.get_sort_icon = get_sort_icon
    g.get_sort_attr = get_sort_attr

    print(g.sort_order)

    form_param = {}
    form_param['city_id'] = g.city_id
    form_param['estate_id'] = g.estate_id
    form_param['district_id'] = g.district_id
    form_param['area_id'] = g.area_id
    form_param['layout'] = g.layout
    form_param['subway'] = g.subway
    form_param['price'] = g.price
    form_param['owner_type'] = g.owner_type
    form_param['square'] = g.square

    g.district_form = ShowDistrictListForCustomerProperyForm(**form_param)
    g.area_form = ShowAreaListForCustomerProperyForm(**form_param)
    g.estate_form = ShowEstateListForCustomerPropertyForm(**form_param)
    g.layout_form = ShowPropertyLayoutForCustomerPropertyForm(**form_param)
    g.subway_form = ShowSubwayListForCustomerPropertyForm(**form_param)
    g.owner_type_form = ShowOwnerTypeListForCustomerPropertyForm(**form_param)
    g.price_form = ShowPriceListForCustomerPropertyForm(**form_param)
    g.square_form = ShowSquareListForCustomerPropertyForm(**form_param)

    g.nav_menu = get_nav_menu1(current_user, PropertyGrade.get_grade_str(g.grade), form_param)

    g.pagination = None
    g.all_properties = None

    property_query = Property.query.filter_by(grade=g.grade)
    if g.estate_id != 0:
        property_query = property_query.filter_by(estate_id=g.estate_id)
    elif g.district_id != 0:
        property_query = property_query.filter_by(district_id=g.district_id)
    else:
        property_query = property_query.filter_by(city_id=g.city_id)
        if g.area_id != 0:
            property_query = property_query.filter_by(area_id=g.area_id)

    # filter by house count
    if g.layout != 0:
        house_count = propery_layouts[g.layout][1]
        if house_count == -1:
            property_query = property_query.filter(Property.count_f > 5)
        else:
            property_query = property_query.filter_by(count_f=house_count)

    # filter by square
    if g.square != 0:
        square_low = square_list[g.square][1]
        square_high = square_list[g.square][2]
        property_query = property_query.filter(Property.square>square_low, Property.square<square_high)

    # filter by price
    if g.price != 0:
        price_low = price_list[g.price][1]
        price_high = price_list[g.price][2]
        property_query = property_query.filter(Property.rent_price > price_low, Property.rent_price < price_high)

    # filter by source
    if g.owner_type != 0:
        property_query = property_query.filter_by(source_id=g.owner_type)

    # order by
    property_query = set_order_by(property_query)

    g.page = request.args.get('page', 1, type=int)
    g.pagination = property_query.paginate(g.page, per_page=10, error_out=False)
    g.all_properties = g.pagination.items


@customer.route('/customer')
@login_required
def index():
    g.pop_menu = get_pop_menu(current_user)
    g.is_search = request.args.get('search', 0, type=int)
    if g.is_search:
        process_search()
    else:
        process_filter()

    return render_template("customer/common.html")



@customer.route('/customer/detail')
@login_required
def property_detail():
    property_id = request.args.get('id', 0, type=int)
    g.property = Property.query.filter_by(property_id=property_id).one()
    # ?? 这里先限制看到的数量为10个
    g.follows = Follow.query.filter_by(property_id=property_id).order_by(Follow.follow_time.desc()).limit(10).all()

    return render_template("customer/detail.html")


@customer.route('/customer/contact')
@login_required
def property_contact():
    property_id = request.args.get('id', 0, type=int)
    g.property = Property.query.filter_by(property_id=property_id).one()
    return render_template("customer/contact.html")


@customer.route('/customer/follow',methods=['POST'])
@login_required
def follow_property():
    property_id = request.values.get('id', 0, type=int)

    follow = Follow()
    follow.follow_content = request.values.get('content', '')
    follow.property_id = property_id
    follow.follow_user_id = current_user.user_id
    db.session.add(follow)
    db.session.commit()

    g.follows = Follow.query.filter_by(property_id=property_id).order_by(Follow.follow_time.desc()).limit(10).all()

    return render_template("customer/follow.html")


@customer.route('/customer/property-map')
@login_required
def property_map():
    g.city_id = 1
    g.district_id = request.args.get('district_id', 0, type=int)
    g.estate_id = request.args.get('estate_id', 0, type=int)
    g.area_id = request.args.get('area_id', 0, type=int)
    g.layout = request.args.get('layout', '')
    g.subway = request.args.get('subway', '')
    g.price = request.args.get('price', '')
    g.owner_type = request.args.get('owner_type', '')
    g.square = request.args.get('square', '')

    form_param = {}
    form_param['city_id'] = g.city_id
    form_param['estate_id'] = g.estate_id
    form_param['district_id'] = g.district_id
    form_param['area_id'] = g.area_id
    form_param['layout'] = g.layout
    form_param['subway'] = g.subway
    form_param['price'] = g.price
    form_param['owner_type'] = g.owner_type
    form_param['square'] = g.square

    g.district_form = ShowDistrictListForCustomerProperyForm(**form_param)
    g.area_form = ShowAreaListForCustomerProperyForm(**form_param)
    g.estate_form = ShowEstateListForCustomerPropertyForm(**form_param)
    g.layout_form = ShowPropertyLayoutForCustomerPropertyForm(**form_param)

    g.subway_form = ShowSubwayListForCustomerPropertyForm(**form_param)
    g.owner_type_form = ShowOwnerTypeListForCustomerPropertyForm(**form_param)
    g.price_form = ShowPriceListForCustomerPropertyForm(**form_param)
    g.square_form = ShowSquareListForCustomerPropertyForm(**form_param)

    g.pop_menu = get_pop_menu(current_user)
    g.nav_menu = get_nav_menu(current_user, "地图房源搜索")
    g.pagination = None
    g.all_properties = None

    property_query = Property.query
    if g.estate_id != 0:
        property_query = property_query.filter_by(estate_id=g.estate_id)
    elif g.district_id != 0:
        property_query = property_query.filter_by(district_id=g.district_id)
    else:
        property_query = property_query.filter_by(city_id=g.city_id)
        if g.area_id != 0:
            property_query = property_query.filter_by(area_id=g.area_id)

    if g.layout!=0:
        house_count = propery_layouts[g.layout][1]
        if house_count==-1:
            property_query = property_query.filter(Property.count_f>5)
        else:
            property_query = property_query.filter_by(count_f=house_count)


    g.page = request.args.get('page', 1, type=int)
    g.pagination = property_query.paginate(g.page, per_page=10, error_out=False)
    g.all_properties = g.pagination.items

    return render_template("customer/property_map.html")

