# -*- coding: utf-8 -*- 

import re
import sys, os
from django import http, template
from django.template import Context, loader
from django.http import HttpResponse
from django.http import HttpResponseRedirect, HttpResponseNotFound, HttpResponseNotModified
from django.conf import settings
from django.core import exceptions, urlresolvers
from django.contrib.auth import authenticate

from pyerp.fnd.shortcuts import fnd_render_to_response
from pyerp.fnd import function as fnd_fun
from pyerp.fnd.models import Responsibility, Function
from pyerp.fnd.gbl import fnd_global
#from pyerp.fnd.auth import authenticate
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
    username = request.POST.get('username', None)
    password = request.POST.get('password', None)
    
    user = authenticate(username=username, password=password)
    
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

# MediaSite
class MediaSite(object):
    """
    公共访问控制器.
    """
    def __init__(self):
        # At compile time, cache the directories to search.
        fs_encoding = sys.getfilesystemencoding() or sys.getdefaultencoding()

        app_media_dirs = []
        for app in settings.INSTALLED_APPS:
            i = app.rfind('.')
            if i == -1:
                m, a = app, None
            else:
                m, a = app[:i], app[i+1:]
            try:
                if a is None:
                    mod = __import__(m, {}, {}, [])
                else:
                    mod = getattr(__import__(m, {}, {}, [a]), a)
            except ImportError, e:
                raise ImproperlyConfigured, 'ImportError %s: %s' % (app, e.args[0])
            media_dir = os.path.join(os.path.dirname(mod.__file__), 'media')
            if os.path.isdir(media_dir):
                app_media_dirs.append(media_dir.decode(fs_encoding))
        # It won't change, so convert it to a tuple to save memory.
        self.app_media_dirs = tuple(app_media_dirs)

    def get_media_sources(self, template_name, template_dirs=None):
        """
        Returns the absolute paths to "template_name", when appended to each
        directory in "template_dirs". Any paths that don't lie inside one of the
        template dirs are excluded from the result set, for security reasons.
        """
        from django.utils._os import safe_join
        if not template_dirs:
            template_dirs = self.app_media_dirs
        for template_dir in template_dirs:
            try:
                yield safe_join(template_dir, template_name)
            except UnicodeDecodeError:
                # The template dir name was a bytestring that wasn't valid UTF-8.
                raise
            except ValueError:
                # The joined path was located outside of template_dir.
                pass

    def was_modified_since(self, header=None, mtime=0, size=0):
        from email.Utils import parsedate_tz, mktime_tz
        try:
            if header is None:
                raise ValueError
            matches = re.match(r"^([^;]+)(; length=([0-9]+))?$", header,
                               re.IGNORECASE)
            header_mtime = mktime_tz(parsedate_tz(matches.group(1)))
            header_len = matches.group(3)
            if header_len and int(header_len) != size:
                raise ValueError
            if mtime > header_mtime:
                raise ValueError
        except (AttributeError, ValueError):
            return True
        return False

    def root(self, request, url):
        import mimetypes
        import stat
        from django.utils.http import http_date
        for filepath in self.get_media_sources(url):
            try:
                statobj = os.stat(filepath)
                if not self.was_modified_since(request.META.get('HTTP_IF_MODIFIED_SINCE'),
                                          statobj[stat.ST_MTIME], statobj[stat.ST_SIZE]):
                    return HttpResponseNotModified()
                mimetype = mimetypes.guess_type(filepath)[0] or 'application/octet-stream'
                contents = open(filepath, 'rb').read()
                response = HttpResponse(contents, mimetype=mimetype)
                response["Last-Modified"] = http_date(statobj[stat.ST_MTIME])
                response['Expires'] = http_date(statobj[stat.ST_MTIME] + (24 * 60 * 60))
                response["Content-Length"] = len(contents)
                return response
            except Exception, e:
                pass
        return http.HttpResponseNotFound('Media is not found.[' + url + ']')

mediasite = MediaSite()


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
