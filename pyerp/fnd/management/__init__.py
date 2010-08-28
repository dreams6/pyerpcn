# -*- coding: utf-8 -*- 

"""
"""

from datetime import datetime, date, timedelta

from django.db.models import get_models, signals

import pyerp.fnd.api.lookup as fnd_lookup
import pyerp.fnd.function as fnd_function
import pyerp.fnd.menu as fnd_menu
import pyerp.fnd.responsibility as fnd_resp
import pyerp.fnd.api.user as fnd_user
from pyerp.fnd import models as fnd_models
from pyerp.fnd.gbl import fnd_global
from pyerp.fnd.profile import fnd_profile
from pyerp.fnd.utils.version import get_svn_revision, get_version

__svnid__ = '$Id$'
__svn__ = get_svn_revision(__name__)

#
#
#
def fnd_init():
    fnd_global.enter_global_management(1)

    # FUNCTION=================================
    fun1 = fnd_function.add("Application", "Applications Form", "pyerp.fnd", "pyerp.fnd.functions.resp.function"                     , None)
    fun2 = fnd_function.add("Functions"  , "Function Form"    , "pyerp.fnd", "pyerp.fnd.functions.resp.function"   , None)
    fun3 = fnd_function.add("Menus"      , "Menus Form"       , "pyerp.fnd", "pyerp.fnd.functions.resp.menu"                     , None)

    # MENU, MENU ITEM==========================
    menu = fnd_menu.add("Application Developer", "Applications Form")
    fnd_menu.additem(menu, 1, "应用程序", "descr1", fun1)
    fnd_menu.additem(menu, 2, "功能部件", "descr2", fun2)
    fnd_menu.additem(menu, 3, "菜单", "descr3", fun3)

    demomenu = fnd_menu.add("实现标准Demo", "Implements Demo")
    fnd_menu.additem(demomenu, 1, "查询", "search",              fnd_function.add("DEMO_SEARCH"            , "Search"             , "pyerp.fnd", "pyerp.fnd.functions.resp.profile" , None))
    fnd_menu.additem(demomenu, 2, "数据维护", "data management", fnd_function.add("DEMO_DATA_MANAGEMENT"   , "Data Management"    , "pyerp.fnd", "pyerp.fnd.functions.resp.profile" , None))
    fnd_menu.additem(demomenu, 3, "LOV", "list of view",         fnd_function.add("DEMO_LOV"               , "LOV"                , "pyerp.fnd", "pyerp.fnd.functions.resp.profile" , None))
    fnd_menu.additem(demomenu, 4, "输入校验", "input validate",  fnd_function.add("DEMO_VALIDATE"          , "Input Validate"     , "pyerp.fnd", "pyerp.fnd.functions.resp.profile" , None))
    fnd_menu.additem(menu, 6, "实现标准Demo", "descr5", None, demomenu)

    # system adminstrator
    ad_menu = fnd_menu.add("Navigator Menu - System Administrator GUI", "Access System Administrator forms and functions")
    c_menu = fnd_menu.add("Concurrent Menu - System Administrator GUI", "System Administrator concurrent processing menu")
    fnd_menu.additem(ad_menu, 0, "Concurrent", "通知", fun1)
    fnd_menu.additem(ad_menu, 1, "Concurrent", "concurrent processing", None, c_menu)
    fnd_menu.additem(c_menu, 1, "请求", "执行Concurrent程序", fnd_function.add("ConcurrentRequest"   , "Concurrent Request"    , "pyerp.fnd", "pyerp.fnd.functions.resp.request" , None))
    fnd_menu.additem(c_menu, 2, "请求集合", "不明", fun2)
    fnd_menu.additem(c_menu, 3, "冲突Domain", "不明", fun3)

    p_menu = fnd_menu.add("Concurrent Programs Menu", "Concurrent Programs")
    fnd_menu.additem(c_menu, 4, "Programs", "Concurrent Programs", None, p_menu)
    fnd_menu.additem(p_menu, 1, "定义", "定义Concurrent Programs", fnd_function.add("ConcurrentProgram"   , "Concurrent Program"    , "pyerp.fnd", "pyerp.fnd.functions.resp.program" , None))
    fnd_menu.additem(p_menu, 2, "执行文件", "注册执行文件", fnd_function.add("ConcurrentExecutable"   , "Concurrent Executable"    , "pyerp.fnd", "pyerp.fnd.functions.resp.executable" , None))
    fnd_menu.additem(p_menu, 3, "类型", "不明", fun3)

    m_menu = fnd_menu.add("Concurrent Manager Menu", "Concurrent Management")
    fnd_menu.additem(c_menu, 5, "Manager", "Concurrent Manager", None, m_menu)
    fnd_menu.additem(m_menu, 1, "管理", "不明", fun1)
    fnd_menu.additem(m_menu, 2, "定义", "定义Manager", fun2)
    fnd_menu.additem(m_menu, 3, "规则", "不明", fun3)

    p_menu = fnd_menu.add("Profile Menu - System Administrator GUI", "Profile Menu")
    fnd_menu.additem(ad_menu, 6, "Profile", "Profile", None, p_menu)
    fnd_menu.additem(p_menu, 0, "定义", "定义Profile", fnd_function.add("DefineProfile"   , "Define Profile"    , "pyerp.fnd", "pyerp.fnd.functions.resp.profile" , None))
    fnd_menu.additem(p_menu, 1, "系统", "系统Profile", fnd_function.add("SystemProfile"   , "System Profile"    , "pyerp.fnd", "pyerp.fnd.functions.resp.profile" , 'system/'))
    fnd_menu.additem(p_menu, 2, "个别", "个别Profile", fnd_function.add("UserProfile"   , "User Profile"    , "pyerp.fnd", "pyerp.fnd.functions.resp.profile" , 'person/'))


    s_menu = fnd_menu.add("Security Menu - System Security GUI", "Security Menu")
    fnd_menu.additem(ad_menu, 7, "安全", "Security", None, s_menu)
    fnd_menu.additem(s_menu, 1, "用户", "User Master",           fnd_function.add("UserMaster"             , "User Master"          , "pyerp.fnd", "pyerp.fnd.functions.resp.user" , None))
    fnd_menu.additem(s_menu, 2, "职责", "Responsibility Master", fnd_function.add("ResponsibilityMaster"   , "Responsibility Master", "pyerp.fnd", "pyerp.fnd.functions.resp.responsibility" , None))

    s_menu = fnd_menu.add("Setup Menu - System Setup GUI", "Setup Menu")
    fnd_menu.additem(ad_menu, 8, "设定", "Setup", None, s_menu)
    fnd_menu.additem(s_menu, 1, "组织", "Organization Master", fun1)
    fnd_menu.additem(s_menu, 2, "活性域", "Flex Field Master", fun2)

    # RESPONSIBILITY
    resp = fnd_resp.add("Application Developer", "Application Developer Responsibility", menu)
    ad_resp = fnd_resp.add("System Adminstrator", "Application Object Library System Adminstrator", ad_menu)

    s_menu = fnd_menu.add("Development Guide - Applications Common Master GUI", "Development Guide")
    fnd_menu.additem(s_menu, 1, "Suggest", "输入提示", fnd_function.add("Suggest"   , "Suggest"    , "pyerp.ak", "pyerp.ak.functions.resp.suggest" ,None))
    ak_resp = fnd_resp.add("Applications Common Master", "Applications Common Master Responsibility", s_menu)

    # USER
    u0 = fnd_user.create_user("u0", "test", "Application Developer User", "pyerp_u0@yahoo.cn")
    u0.responsibilities.add(resp)            # "Application Developer Responsibility"
    u0.responsibilities.add(ad_resp)         # "System Adminstrator Responsibility"
    u0.responsibilities.add(ak_resp)         # "Applications Common Master Responsibility"

    u1 = fnd_user.create_user("u1", "test", "Application Developer User", "u1@localhost.com")
    u1.responsibilities.add(resp)      # "Application Developer Responsibility"

    u2 = fnd_user.create_user("u2", "test", "Application Developer User", "u2@localhost.com", pwd_expiration_type=1, pwd_lifespan=10)
    u2.responsibilities.add(resp)            # "Application Developer Responsibility"

    u3 = fnd_user.create_user("u3", "test", "Application Developer User", "u3@localhost.com", pwd_expiration_type=2, pwd_lifespan=3)
    u3.responsibilities.add(resp)            # "Application Developer Responsibility"

    u4 = fnd_user.create_user("u4", "test", "Application Developer User", "u4localhost.com", end_date_active=(date.today()-timedelta(days=1)) )
    u4.responsibilities.add(resp)            # "Application Developer Responsibility"

    # resp = fnd_resp.add("Application Developer", "Application Developer Responsibility", menu)
    fnd_global.set_attr('user_id', u0.id)
    fnd_global.set_resp_id(ad_resp.id)

    # PROFILE
    fnd_profile.define("org_id")
    fnd_profile.save("org_id", "103", "SITE", 1)
    # print fnd_profile.value("org_id")
    fnd_profile.save("org_id", "120", "RESP", ad_resp.id)
    # print fnd_profile.value("org_id")
    fnd_profile.save("org_id", "130", "USER", u0.id)
    # print fnd_profile.value("org_id")

    # 登录user Function
    fun1 = fnd_function.add("fnd.Main", "导航菜单", "pyerp.fnd", "pyerp.fnd.functions.user.main"   , None)
    fm = fnd_models.FuncMapping()
    fm.regex_pattern = '^main/'
    fm.type = 'user'
    fm.seq = 1
    fm.function = fun1
    # ==============================
    fm.created_by = fnd_global.user_id
    fm.last_updated_by = fnd_global.user_id
    # ==============================
    fm.save()
    fm = fnd_models.FuncMapping()
    fm.regex_pattern = '^$'
    fm.type = 'user'
    fm.seq = 100
    fm.function = fun1
    # ==============================
    fm.created_by = fnd_global.user_id
    fm.last_updated_by = fnd_global.user_id
    # ==============================
    fm.save()

    fun1 = fnd_function.add("fnd.ChangePwd", "修改密码", "pyerp.fnd", "pyerp.fnd.functions.user.changepwd"   , None)
    fm = fnd_models.FuncMapping()
    fm.regex_pattern = '^changepwd/'
    fm.type = 'user'
    fm.seq = 2
    fm.function = fun1
    # ==============================
    fm.created_by = fnd_global.user_id
    fm.last_updated_by = fnd_global.user_id
    # ==============================
    fm.save()
    
    fun1 = fnd_function.add("fnd.Feedback", "用户反馈", "pyerp.fnd", "pyerp.fnd.functions.user.feedback"   , None)
    fm = fnd_models.FuncMapping()
    fm.regex_pattern = '^feedback/'
    fm.type = 'user'
    fm.seq = 3
    fm.function = fun1
    # ==============================
    fm.created_by = fnd_global.user_id
    fm.last_updated_by = fnd_global.user_id
    # ==============================
    fm.save()

    fun1 = fnd_function.add("fnd.MailBox", "站内信", "pyerp.fnd", "pyerp.fnd.functions.user.mailbox"   , None)
    fm = fnd_models.FuncMapping()
    fm.regex_pattern = '^mailbox/'
    fm.type = 'user'
    fm.seq = 4
    fm.function = fun1
    # ==============================
    fm.created_by = fnd_global.user_id
    fm.last_updated_by = fnd_global.user_id
    # ==============================
    fm.save()

    fun1 = fnd_function.add("fnd.Notices", "通知", "pyerp.fnd", "pyerp.fnd.functions.user.notification"   , None)
    fm = fnd_models.FuncMapping()
    fm.regex_pattern = '^notices/'
    fm.type = 'user'
    fm.seq = 5
    fm.function = fun1
    # ==============================
    fm.created_by = fnd_global.user_id
    fm.last_updated_by = fnd_global.user_id
    # ==============================
    fm.save()
    
    fun1 = fnd_function.add("fnd.Help", "帮助", "pyerp.fnd", "pyerp.fnd.functions.user.help"   , None)
    fm = fnd_models.FuncMapping()
    fm.regex_pattern = '^help/'
    fm.type = 'user'
    fm.seq = 6
    fm.function = fun1
    # ==============================
    fm.created_by = fnd_global.user_id
    fm.last_updated_by = fnd_global.user_id
    # ==============================
    fm.save()

    
    fun1 = fnd_function.add("fnd.Login", "登录", "pyerp.fnd", "pyerp.fnd.functions.pub.login"   , None)
    fm = fnd_models.FuncMapping()
    fm.regex_pattern = '^login/$'
    fm.type = 'pub'
    fm.seq = 1
    fm.function = fun1
    # ==============================
    fm.created_by = fnd_global.user_id
    fm.last_updated_by = fnd_global.user_id
    # ==============================
    fm.save()


    fun1 = fnd_function.add("fnd.Lougot", "退出", "pyerp.fnd", "pyerp.fnd.functions.pub.logout"   , None)
    fm = fnd_models.FuncMapping()
    fm.regex_pattern = '^logout/$'
    fm.type = 'pub'
    fm.seq = 2
    fm.function = fun1
    # ==============================
    fm.created_by = fnd_global.user_id
    fm.last_updated_by = fnd_global.user_id
    # ==============================
    fm.save()


    fun1 = fnd_function.add("fnd.Index", "首页", "pyerp.fnd", "pyerp.fnd.functions.pub.index"   , None)
    fm = fnd_models.FuncMapping()
    fm.regex_pattern = '^.*'
    fm.type = 'pub'
    fm.seq = 3
    fm.function = fun1
    # ==============================
    fm.created_by = fnd_global.user_id
    fm.last_updated_by = fnd_global.user_id
    # ==============================
    fm.save()



    # 定义用户首页profile
    fnd_profile.define("user_home_page")


    fnd_global.leave_global_management()
    
def fnd_init_currency():
    fnd_global.enter_global_management(1)
    import os
    file_name = os.path.join(os.path.dirname(__file__), 'currencies_us_ja.txt')
    datafile = open(file_name, "r")
    lines = datafile.readlines()
    for line in lines:
        # print line
        fields = line.split("\t")
        currency = fnd_models.Currency()
        currency.code = fields[0]
        currency.language = fields[1]
        if fields[1]=="JA":
          currency.symbol = "￥"
        else:
          currency.symbol = "$"
        currency.name = fields[2]
        currency.description = fields[3]
        currency.created_by = fnd_global.user_id
        currency.last_updated_by = fnd_global.user_id
        currency.save()
    datafile.close()
    fnd_global.leave_global_management()
    
def fnd_init_notice():
    nt = fnd_models.NoticeType()
    nt.label = "messages_deleted"
    nt.display = "ddddd"
    nt.description = "description"
    nt.default = 1
    nt.save()
    pass

def fnd_init_concurrent():
    import os
    fnd_global.enter_global_management(1)
    ce = fnd_models.ConcurrentExecutable()
    ce.name = "hello"
    ce.method = "django_script"
    ce.file = "pyerp.ak.programs.hello.main"
    ce.save()
    cp = fnd_models.ConcurrentProgram()
    cp.executable = ce
    cp.name = "hello"
    cp.output_file_mime = "txt"
    cp.save()
    
    # 清空ConcurrentRequest输入/输出目录
    io_path = os.path.join(os.path.expanduser("~"), ".pyerp", "ConcurrentRequest")
    # Delete everything reachable from the directory named in 'top',
    # assuming there are no symbolic links.
    # CAUTION:  This is dangerous!  For example, if top == '/', it
    # could delete all your disk files.
    import os
    if os.path.exists(io_path):
        for root, dirs, files in os.walk(io_path, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))

    fnd_global.leave_global_management()


# 
#
def initialization(app, created_models, verbosity, **kwargs):
    import pyerp.fnd.models as fnd_models
    if fnd_models.LookUpNode in created_models and kwargs.get('interactive', True):
        msg = "\nYou just installed Fnd module, which means you don't have " \
        "initialization data installed.\nWould you like to create them now? (yes/no): "
        confirm = raw_input(msg)
        while 1:
            if confirm not in ('yes', 'no'):
                confirm = raw_input('Please enter either "yes" or "no": ')
                continue
            if confirm == 'yes':
                # call_command("createsuperuser", interactive=True)
                fnd_init()
                break
    # 货币
    if fnd_models.Currency in created_models and kwargs.get('interactive', True):
        fnd_init_currency()

    # 通知
    if fnd_models.NoticeType in created_models and kwargs.get('interactive', True):
        fnd_init_notice()

    # concurrent request
    if fnd_models.ConcurrentRequest in created_models and kwargs.get('interactive', True):
        fnd_init_concurrent()


signals.post_syncdb.connect(initialization,
        sender=fnd_models, dispatch_uid = "pyerp.fnd.management.initialization")
