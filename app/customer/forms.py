from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField, \
    SelectField, TextAreaField, IntegerField, FloatField, DateField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from flask import render_template, redirect, request, url_for, flash
from ..models_property import City, District, Area, Estate, PropertyType, PropertySource

class ShowDistrictListForCustomerProperyForm(Form):
    district = SelectField('行政区域', id="district_selection")

    def __init__(self, *args, **kwargs):
        super(ShowDistrictListForCustomerProperyForm, self).__init__(*args, **kwargs)
        city_id = kwargs['city_id']
        district_id = kwargs['district_id']
        self.district.choices = [(district.district_id, district.district_name)
                             for district in District.query.filter_by(city_id=city_id).all()]
        item_all = ( 0,"全部")
        self.district.choices.insert(0,item_all)
        if district_id==0:
            self.district.data = str(item_all[0])
        else:
            self.district.data = str(district_id)


class ShowAreaListForCustomerProperyForm(Form):
    area = SelectField('房源区域', id="area_selection")

    def __init__(self, *args, **kwargs):
        super(ShowAreaListForCustomerProperyForm, self).__init__(*args, **kwargs)
        city_id = kwargs['city_id']
        area_id = kwargs['area_id']
        self.area.choices = [( area.area_id, area.area_name)
                             for area in Area.query.filter_by(city_id=city_id).all()]

        item_all = ( 0, "全部")
        self.area.choices.insert(0, item_all)
        if area_id == 0:
            self.area.data = str(item_all[0])
        else:
            self.area.data = str(area_id)


class ShowEstateListForCustomerPropertyForm(Form):
    estate = SelectField('楼盘', id="estate_selection")

    def __init__(self, *args, **kwargs):
        super(ShowEstateListForCustomerPropertyForm, self).__init__(*args, **kwargs)
        district_id = kwargs['district_id']
        estate_id = kwargs['estate_id']
        area_id = kwargs['area_id']
        self.estate.choices = [(estate.estate_id, estate.estate_name)
                             for estate in Estate.query.filter_by(district_id=district_id).all()]
        item_all = ( 0,"全部")
        self.estate.choices.insert(0,item_all)
        if district_id==0:
            self.estate.data = str(item_all[0])
        else:
            self.estate.data = str(estate_id)


propery_layouts = [
    ("全部", 0),
    ("1房",  1),
    ("2房",  2),
    ("3房",  3),
    ("4房",  4),
    ("5房",  5),
    ("5房以上",-1),
]

class ShowPropertyLayoutForCustomerPropertyForm(Form):
    layout = SelectField('房型', id="layout_selection")

    def __init__(self, *args, **kwargs):
        super(ShowPropertyLayoutForCustomerPropertyForm, self).__init__(*args, **kwargs)
        layout = kwargs['layout']
        self.layout.choices = [(i, layout[0])
                             for i,layout in enumerate(propery_layouts)]
        if not layout:
            self.layout.data = self.layout.choices[0][0]
        else:
            self.layout.data = str(layout)

subways = [
    "全部",
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
        subway_sel = kwargs['subway']

        self.subway.choices = [(subway, subway)
                             for subway in subways]
        if not subway_sel:
            self.subway.data = self.subway.choices[0][0]
        else:
            self.subway.data = subway_sel


square_list = [
    ("全部",         -1, -1 ),
    ("50平米以下",   0,50),
    ("50-100平米",   50,100),
    ("100-200平米",  100,200),
    ("200平米以上", 200,100000),
]


class ShowSquareListForCustomerPropertyForm(Form):
    square = SelectField('面积', id="square_selection")

    def __init__(self, *args, **kwargs):
        super(ShowSquareListForCustomerPropertyForm, self).__init__(*args, **kwargs)
        square_sel = kwargs['square']

        self.square.choices = [(i, square[0])
                             for i,square in enumerate(square_list)]
        if not square_sel:
            self.square.data = self.square.choices[0][0]
        else:
            self.square.data = str(square_sel)


class ShowOwnerTypeListForCustomerPropertyForm(Form):
    owner_type = SelectField('业主类型', id="owner_type_selection")

    def __init__(self, *args, **kwargs):
        super(ShowOwnerTypeListForCustomerPropertyForm, self).__init__(*args, **kwargs)
        owner_type_sel = kwargs['owner_type']

        self.owner_type.choices = [(str(source.source_id), source.source_name)
                             for source in PropertySource.query.all()]

        item_all = ( 0,"全部")
        self.owner_type.choices.insert(0,item_all)
        if not owner_type_sel:
            self.owner_type.data = self.owner_type.choices[0][0]
        else:
            self.owner_type.data = str(owner_type_sel)


price_list = [
    ("全部",        -1,-1),
    ("800元以下",   0,800),
    ("800-1500元",  800,1500),
    ("1500-2000元", 1500,2000),
    ("2000-3000元", 2000,3000),
    ("3000-5000元", 3000,5000),
    ("5000-6500元", 5000,6500),
    ("6500-8000元", 6500,8000),
    ("8000元以上",  8000,10000000),
]

class ShowPriceListForCustomerPropertyForm(Form):
    price = SelectField('价格', id="price_selection")

    def __init__(self, *args, **kwargs):
        super(ShowPriceListForCustomerPropertyForm, self).__init__(*args, **kwargs)
        price_range = kwargs['price']

        self.price.choices = [(i, price[0])
                             for i,price in enumerate(price_list)]
        if not price_range:
            self.price.data = self.price.choices[0][0]
        else:
            self.price.data = str(price_range)
