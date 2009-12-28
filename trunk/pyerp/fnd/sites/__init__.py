# -*- coding: utf-8 -*- 

import re

from django import http, template
from django.template import Context, loader
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.conf import settings
from django.core import exceptions, urlresolvers

from pyerp.fnd.shortcuts import fnd_render_to_response
from pyerp.fnd import function as fnd_fun
from pyerp.fnd.models import Responsibility, Function
from pyerp.fnd.gbl import fnd_global
from pyerp.fnd.auth import authenticate
from pyerp.fnd.auth import login as login_session
from pyerp.fnd.auth import has_resp
from pyerp.fnd.auth import fun_in_resp
from pyerp.fnd.views import display_http_403

from pyerp.fnd.functions.pub.login.views import display_login_form


LOGIN_FORM_KEY = 'this_is_the_login_form'


#
# 
#
def is_login_request(request):
    return request.POST.has_key(LOGIN_FORM_KEY)

#
# 
#
def login(request):
    """
    Displays the login form for the given HttpRequest.
    """
    from pyerp.fnd.models import User
    from datetime import datetime, date, timedelta

    # Check that the user accepts cookies.
    if not request.session.test_cookie_worked():
        message = "您好像没有配置您的游览器,使之开启Cookie功能.请开启cookie功能."
        return display_login_form(request, message)
    else:
        request.session.delete_test_cookie()

    # Check the password.
    login_id = request.POST.get('login_id', None)
    password = request.POST.get('password', None)
    user = authenticate(login_id=login_id, password=password)
    if user is None:
        message = "请输入正确的用户名和密码.请注意,用户名/密码是大小写敏感的."
        return display_login_form(request, message)
    # The user data is correct; 
    # 密码是否过期
    if user.pwd_expiration_type == 1:   # 天数
        if (date.today()-user.pwd_begin_date).days >= user.pwd_lifespan:  # 密码过期
            # 随机重置密码()
            new_pwd = user.reset_random_password()
            # TODO 保留 发送邮件()
            message = "您的密码已经过期.请联系管理员."
            return display_login_form(request, message)
        elif (date.today() - user.pwd_begin_date).days + 15 > user.pwd_lifespan:  # 15天 将要过期
            # TODO session['pwd_expiration_alert'] = "您的密码即将过期,请及时修改你的密码."
            pass
    elif user.pwd_expiration_type == 2:   # 访问次数
        if user.pwd_accesses >= user.pwd_lifespan:
            # 随机重置密码()
            new_pwd = user.reset_random_password()
            # TODO 保留 发送邮件()
            message = "您的密码已经过期.请联系管理员."
            return display_login_form(request, message)
        elif user.pwd_accesses+10 >= user.pwd_lifespan:
            # TODO session['pwd_expiration_alert'] = "您的密码即将过期,请及时修改你的密码."
            pass

    # 将上次登录时间保存在session中
    request.session['last_login'] = user.last_login

    # log in the user in and continue.
    login_session(request, user)

    return HttpResponseRedirect(request.get_full_path())

# ProtectedRespSite
class ProtectedRespSite(object):
    
    """
    基于职责访问控制器.
    """

    def root(self, request,resp_id, menu_id, function_id, url):
        """
        0, 检查用户是否可以访问该资源.
        1, 取得指定function的urlconf信息.
        2, 与url进行匹配.
        3, 执行相应的view.
        """
        if request.method == 'GET' and not request.path.endswith('/'):
            return HttpResponseRedirect(request.path + '/')

        # 执行login处理
        if is_login_request(request):
            return login(request)

        # 没有Login时,显示Login画面
        if not request.user.is_authenticated():
            return display_login_form(request, '')

        # 取得职责
        try:
            resp = Responsibility.objects.get(pk=resp_id)
        except Responsibility.DoesNotExist:
            raise http.Http404('Responsibility is not found.[' + resp_id + ']')

        # 取得function 
        try:
            function = Function.objects.get(pk=function_id)
        except Function.DoesNotExist:
            raise http.Http404('Function is not found.[' + function_id + ']')

        # 判定用户是否具备指定的职责
        if not has_resp(request, resp):
            # TODO  from django.core.exceptions import PermissionDenied
            return display_http_403(request, "用不能访问该职责")
        
        # 判定是否可以执行指定的function
        if not fun_in_resp(function, resp):
            return display_http_403(request, "用不能访问该功能")

        # 设定fnd全局变量
        fnd_global.set_resp_id(resp.id)
        fnd_global.set_menu_id(menu_id)
        fnd_global.set_function(function)

        # 根据function的url配置,执行请求.  
        resolver = urlresolvers.RegexURLResolver(r'', function.urlconf)
        callback, callback_args, callback_kwargs = resolver.resolve(url)
        return callback(request, *callback_args, **callback_kwargs)

respsite = ProtectedRespSite()

# ProtectedUserSite
class ProtectedUserSite(object):
    """
    基于用户的访问控制器.
    """

    def root(self, request, url):
        if request.method == 'GET' and not request.path.endswith('/'):
            return HttpResponseRedirect(request.path + '/')
        
        # 执行login处理
        if is_login_request(request):
            return login(request)

        # 没有Login时,显示Login画面
        if not request.user.is_authenticated():
            return display_login_form(request, '')

        # 根据function的url配置,执行请求. 
        resolver = urlresolvers.RegexURLResolver(r'', 'pyerp.fnd.sites.user_urls')
        callback, callback_args, callback_kwargs = resolver.resolve(url)
        fnd_global.set_function(callback_kwargs.pop('func'))
        return callback(request, *callback_args, **callback_kwargs)

usersite = ProtectedUserSite()

# PublicSite
class PublicSite(object):
    """
    公共访问控制器.
    """

    def root(self, request, url):
        if request.method == 'GET' and not request.path.endswith('/'):
            return HttpResponseRedirect(request.path + '/')
        # TODO 一个替代的方案
        # 类似于职责的功能,
        # 把一个个('^xxxx', include('rootsite.root'))保存在数据库中
        # 并在运行时,加载到一个指定的urls中,然后使用这个urls作为Resolver
        # 
#        from pyerp.fnd.functions.pub import urls
#        from django.conf.urls.defaults import patterns, include
#        urls.urlpatterns += patterns('',
#                ('^xxxx', include('rootsite.root') ),
#            )
#        print urls.urlpatterns
        
        # 根据function的url配置,执行请求. 
        resolver = urlresolvers.RegexURLResolver(r'', 'pyerp.fnd.sites.pub_urls')
        callback, callback_args, callback_kwargs = resolver.resolve(url)
        fnd_global.set_function(callback_kwargs.pop('func'))
        return callback(request, *callback_args, **callback_kwargs)

pubsite = PublicSite()

# RootSite
class RootSite(object):
    """
    根访问控制器.
    """
    def root(self, request, url):
        return HttpResponseRedirect(fnd_global.context_prefix + 
                                    settings.FND_PUB_SITE_PREFIX + url)

rootsite = RootSite()
