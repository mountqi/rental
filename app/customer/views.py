from flask import render_template, redirect, request, url_for, flash, g
from flask_login import login_user, logout_user, login_required, \
    current_user

from . import customer
from .. import db
from .menu_factory import get_pop_menu, get_nav_menu

from ..models_property import City, District, Area, Estate, Property, Follow

from .forms import ShowDistrictListForCustomerProperyForm, ShowAreaListForCustomerProperyForm, \
    ShowEstateListForCustomerPropertyForm, ShowPropertyLayoutForCustomerPropertyForm, \
    ShowSubwayListForCustomerPropertyForm, ShowOwnerTypeListForCustomerPropertyForm, \
    ShowPriceListForCustomerPropertyForm, ShowSquareListForCustomerPropertyForm

@customer.route('/customer')
@login_required
def index():

    g.city_id = 1
    g.district_id = request.args.get('district_id', 0, type=int)
    g.estate_id = request.args.get('estate_id', 0, type=int)
    g.area_id = request.args.get('area_id', 0, type=int)

    form_param = {}
    form_param['city_id'] = g.city_id
    form_param['estate_id'] = g.estate_id
    form_param['district_id'] = g.district_id
    form_param['area_id'] = g.area_id
    form_param['url'] = "customer.index"

    g.district_form = ShowDistrictListForCustomerProperyForm(**form_param)
    g.area_form = ShowAreaListForCustomerProperyForm(**form_param)
    g.estate_form = ShowEstateListForCustomerPropertyForm(**form_param)
    g.layout_form = ShowPropertyLayoutForCustomerPropertyForm(**form_param)

    g.subway_form = ShowSubwayListForCustomerPropertyForm(**form_param)
    g.owner_type_form = ShowOwnerTypeListForCustomerPropertyForm(**form_param)
    g.price_form = ShowPriceListForCustomerPropertyForm(**form_param)
    g.square_form = ShowSquareListForCustomerPropertyForm(**form_param)

    g.pop_menu=get_pop_menu(current_user)
    g.nav_menu=get_nav_menu(current_user,"高端认证房源")
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

    g.page = request.args.get('page', 1, type=int)
    g.pagination = property_query.paginate(g.page, per_page=10, error_out=False)
    g.all_properties = g.pagination.items

    return render_template("customer/common1.html")


@customer.route('/customer/property-map')
@login_required
def property_map():
    g.city_id = 1
    g.district_id = request.args.get('district_id', 0, type=int)
    g.estate_id = request.args.get('estate_id', 0, type=int)
    g.area_id = request.args.get('area_id', 0, type=int)

    form_param = {}
    form_param['city_id'] = g.city_id
    form_param['estate_id'] = g.estate_id
    form_param['district_id'] = g.district_id
    form_param['area_id'] = g.area_id
    form_param['url'] = "customer.index"

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

    g.page = request.args.get('page', 1, type=int)
    g.pagination = property_query.paginate(g.page, per_page=10, error_out=False)
    g.all_properties = g.pagination.items

    return render_template("customer/property_map.html")

