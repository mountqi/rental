from ..models_user import Permission


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


def get_nav_menu( user, active_title):
    nav_menu = []
    nav_menu.append(["高端认证房源", "customer.index", False])
    nav_menu.append(["高性价比广告房源", "customer.index", False])
    nav_menu.append(["中低端未认证房源", "customer.index", False])
    nav_menu.append(["风险业主名单", "customer.index", False])
    nav_menu.append(["地图房源搜索", "customer.property_map", False])
    return set_active_nav_menu(nav_menu,active_title)
