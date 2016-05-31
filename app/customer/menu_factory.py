from ..models_user import Permission
from ..models_property import PropertyGrade
from flask import url_for

def get_pop_menu(user):
    menu = []
    menu.append(("退出", "auth.logout", "menu"))
    pop_menu = {
        "menu" : menu
    }
    return pop_menu


def set_active_nav_menu(tab_menu,active_title):
    for menu in tab_menu:
        if menu[0] == active_title:
            menu[2]=True
    return tab_menu

class HouseGrade:
    HIGH_VERIFIED = "高端认证房源"
    HIGH_ADS = "高性价比广告房源"
    LOW_NO_VERIFIED = "中低端未认证房源"
    BLACKLIST = "风险业主名单"


def get_nav_menu( user, active_title ):
    nav_menu = []
    nav_menu.append(["高端认证房源", "customer.index", False])
    nav_menu.append(["高性价比广告房源", "customer.index", False])
    nav_menu.append(["中低端未认证房源", "customer.index", False])
    nav_menu.append(["风险业主名单", "customer.index", False])
    nav_menu.append(["地图房源搜索", "customer.property_map", False])
    return set_active_nav_menu(nav_menu,active_title)


def get_nav_menu1( user, active_title, param ):
    nav_menu = []
    nav_menu.append([PropertyGrade.get_grade_str(PropertyGrade.HIGH_VERIFIED), url_for("customer.index",grade=PropertyGrade.HIGH_VERIFIED,**param), False])
    nav_menu.append([PropertyGrade.get_grade_str(PropertyGrade.HIGH_ADS), url_for("customer.index",grade=PropertyGrade.HIGH_ADS,**param), False])
    nav_menu.append([PropertyGrade.get_grade_str(PropertyGrade.LOW_NO_VERIFIED), url_for("customer.index",grade=PropertyGrade.LOW_NO_VERIFIED,**param), False])
    nav_menu.append([PropertyGrade.get_grade_str(PropertyGrade.BLACKLIST), url_for("customer.index",grade=PropertyGrade.BLACKLIST,**param), False])
    nav_menu.append(["地图房源搜索", "", False])
    return set_active_nav_menu(nav_menu,active_title)
