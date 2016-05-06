from ..user_models import Permission


def get_nav_menu(user):
    menu = []
    if Permission.is_admin_backend_management(user.role.permissions):
        menu.append( ("后台管理","admin.users","menu") )
    if Permission.is_admin_IT(user.role.permissions):
        menu.append( ("系统维护","admin.undone","menu") )
    if Permission.is_admin_house_management(user.role.permissions):
        menu.append( ("房源维护","admin.undone","menu") )
    if Permission.is_admin_customer_management(user.role.permissions):
        menu.append( ("用户管理","admin.personal_customers","menu") )

    if len(menu):
        menu.append(("", "", "sep"))
    menu.append(("后台首页", "admin.index", "menu"))
    nav_menu = {
        "title": "后台导航",
        "menu" : menu
    }
    return nav_menu


def get_tab_menu(topic,user,active_title):
    if topic == "users":
        return get_tab_menu_admin_users(user, active_title)
    elif topic == "customers":
        return get_tab_menu_admin_customers(user, active_title)
    return None


def set_active_tab_menu(tab_menu,active_title):
    for menu in tab_menu:
        if menu[0] == active_title:
            menu[2]=True
    return tab_menu


def get_tab_menu_admin_users(user, active_title):
    tab_menu = []
    if user.can( Permission.ADD_MOD_PMSN_GRP ):
        tab_menu.append(["管理员", "admin.users", False])
    if user.can(Permission.ADD_MOD_ADMIN_USER):
        tab_menu.append(["权限组", "admin.rolegroups", False])
    return set_active_tab_menu(tab_menu,active_title)


def get_tab_menu_admin_customers(user, active_title):
    tab_menu = []
    if user.can(Permission.ADD_MOD_CUSTOMER):
        tab_menu.append(["个人用户", "admin.personal_customers", False])
        tab_menu.append(["公司用户", "admin.corp_customers", False])
        tab_menu.append(["缴费退费", "admin.fee_records", False])
        tab_menu.append(["收费标准", "admin.fee_standards", False])
    return set_active_tab_menu(tab_menu,active_title)