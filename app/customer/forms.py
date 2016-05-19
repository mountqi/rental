from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField, \
    SelectField, TextAreaField, IntegerField, FloatField, DateField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from flask import render_template, redirect, request, url_for, flash
from ..models_property import City, District, Area, Estate, PropertyType, PropertySource

def create_customer_property_url( url, city_id, district_id, estate_id,  area_id  ):
    return url_for( url, city_id=city_id, district_id=district_id, estate_id=estate_id,
                   area_id=area_id )


class ShowDistrictListForCustomerProperyForm(Form):
    district = SelectField('行政区域', id="district_selection")

    def __init__(self, *args, **kwargs):
        super(ShowDistrictListForCustomerProperyForm, self).__init__(*args, **kwargs)
        city_id = kwargs['city_id']
        district_id = kwargs['district_id']
        estate_id = kwargs['estate_id']
        area_id = kwargs['area_id']
        url = kwargs['url']
        self.district.choices = [(create_customer_property_url(url,city_id,district.district_id,estate_id,area_id), district.district_name)
                             for district in District.query.filter_by(city_id=city_id).all()]
        item_all = (create_customer_property_url( url, city_id, 0, estate_id, area_id ),"全部")
        self.district.choices.insert(0,item_all)
        if district_id==0:
            self.district.data = item_all[0]
        else:
            self.district.data = create_customer_property_url( url, city_id, district_id, estate_id, area_id )


class ShowAreaListForCustomerProperyForm(Form):
    area = SelectField('房源区域', id="area_selection")

    def __init__(self, *args, **kwargs):
        super(ShowAreaListForCustomerProperyForm, self).__init__(*args, **kwargs)
        city_id = kwargs['city_id']
        district_id = kwargs['district_id']
        estate_id = kwargs['estate_id']
        area_id = kwargs['area_id']
        url = kwargs['url']
        self.area.choices = [(create_customer_property_url(url, city_id,district_id,estate_id, area.area_id), area.area_name)
                             for area in Area.query.filter_by(city_id=city_id).all()]

        item_all = (create_customer_property_url(url,city_id, district_id,estate_id, 0), "全部")
        self.area.choices.insert(0, item_all)
        if area_id == 0:
            self.area.data = item_all[0]
        else:
            self.area.data = create_customer_property_url(url,city_id, district_id, estate_id, area_id)


class ShowEstateListForCustomerPropertyForm(Form):
    estate = SelectField('楼盘', id="estate_selection")

    def __init__(self, *args, **kwargs):
        super(ShowEstateListForCustomerPropertyForm, self).__init__(*args, **kwargs)
        city_id = kwargs['city_id']
        district_id = kwargs['district_id']
        estate_id = kwargs['estate_id']
        area_id = kwargs['area_id']
        url = kwargs['url']
        self.estate.choices = [(create_customer_property_url(url, city_id,district_id,estate.estate_id, area_id), estate.estate_name)
                             for estate in Estate.query.filter_by(district_id=district_id).all()]
        item_all = (create_customer_property_url( url, city_id, district_id, 0, area_id  ),"全部")
        self.estate.choices.insert(0,item_all)
        if district_id==0:
            self.estate.data = item_all[0]
        else:
            self.estate.data = create_customer_property_url( url, city_id, district_id,estate_id, area_id )


propery_layouts = [
    "所有",
    "1室1厅",
    "2室1厅",
    "3室1厅",
    "3室2厅",
    "4室1厅",
    "4室2厅",
    "其它"
]

class ShowPropertyLayoutForCustomerPropertyForm(Form):
    layout = SelectField('房型', id="layout_selection")

    def __init__(self, *args, **kwargs):
        super(ShowPropertyLayoutForCustomerPropertyForm, self).__init__(*args, **kwargs)
        city_id = kwargs['city_id']
        district_id = kwargs['district_id']
        estate_id = kwargs['estate_id']
        area_id = kwargs['area_id']
        url = kwargs['url']
        self.layout.choices = [(create_customer_property_url(url, city_id,district_id,estate_id, area_id), layout)
                             for layout in propery_layouts]


subways = [
    "所有",
    "1号线",
    "2号线",
    "3号线",
    "4号线",
    "5号线",
    "6号线",
    "7号线",
    "8号线",
    "9号线",
    "10号线",
    "11号线",
    "12号线",
    "13号线",
    "14号线",
    "15号线",
    "16号线",
    "17号线",
    "18号线"
]

class ShowSubwayListForCustomerPropertyForm(Form):
    subway = SelectField('地铁', id="subway_selection")

    def __init__(self, *args, **kwargs):
        super(ShowSubwayListForCustomerPropertyForm, self).__init__(*args, **kwargs)
        city_id = kwargs['city_id']
        district_id = kwargs['district_id']
        estate_id = kwargs['estate_id']
        area_id = kwargs['area_id']
        url = kwargs['url']
        self.subway.choices = [(create_customer_property_url(url, city_id,district_id,estate_id, area_id), subway)
                             for subway in subways]


squares = [
    "所有",
    "50平米以下",
    "50-100平米",
    "100-200平米",
    "200平米以上",
]

class ShowSquareListForCustomerPropertyForm(Form):
    square = SelectField('面积', id="square_selection")

    def __init__(self, *args, **kwargs):
        super(ShowSquareListForCustomerPropertyForm, self).__init__(*args, **kwargs)
        city_id = kwargs['city_id']
        district_id = kwargs['district_id']
        estate_id = kwargs['estate_id']
        area_id = kwargs['area_id']
        url = kwargs['url']
        self.square.choices = [(create_customer_property_url(url, city_id,district_id,estate_id, area_id), square)
                             for square in squares]


owner_types = [
    "所有",
    "M 源涞国际",
    "L 个人业主",
    "S 比利华",
]

class ShowOwnerTypeListForCustomerPropertyForm(Form):
    owner_type = SelectField('业主类型', id="owner_type_selection")

    def __init__(self, *args, **kwargs):
        super(ShowOwnerTypeListForCustomerPropertyForm, self).__init__(*args, **kwargs)
        city_id = kwargs['city_id']
        district_id = kwargs['district_id']
        estate_id = kwargs['estate_id']
        area_id = kwargs['area_id']
        url = kwargs['url']
        self.owner_type.choices = [(create_customer_property_url(url, city_id,district_id,estate_id, area_id), owner_type)
                             for owner_type in owner_types]


price_list = [
    "所有",
    "5000以下",
    "5000-10000",
    "10000-20000",
    "20000以上",
]

class ShowPriceListForCustomerPropertyForm(Form):
    price = SelectField('价格', id="price_selection")

    def __init__(self, *args, **kwargs):
        super(ShowPriceListForCustomerPropertyForm, self).__init__(*args, **kwargs)
        city_id = kwargs['city_id']
        district_id = kwargs['district_id']
        estate_id = kwargs['estate_id']
        area_id = kwargs['area_id']
        url = kwargs['url']
        self.price.choices = [(create_customer_property_url(url, city_id,district_id,estate_id, area_id), price)
                             for price in price_list]



