# -*- coding: utf-8 -*- 

import time

from django.conf import settings
from django.utils.cache import patch_vary_headers
from django.utils.http import cookie_date
from pyerp.fnd.gbl import fnd_global


#import gbl as fnd_global                    # TODO:这种引用方法和上边的方法存在着fnd_global(这个程序中设定的值，在其他的地方(sites.py)取得不到)下的变量不同地址的问题，需要找到原因

class LazyUser(object):
    def __get__(self, request, obj_type=None):
        if not hasattr(request, '_cached_user'):
            from auth import get_user
            request._cached_user = get_user(request)
        return request._cached_user

class FndGlobalMiddleware(object):

    def process_request(self, request):
        """
         1, 处理session
         2, 处理auth
         3, 初始化fnd_global
        """
        # start session===============================
        engine = __import__(settings.SESSION_ENGINE, {}, {}, [''])
        session_key = request.COOKIES.get(settings.SESSION_COOKIE_NAME, None)
        request.session = engine.SessionStore(session_key)
        # end session=================================
        # start auth=================================
        request.__class__.user = LazyUser()
        # end auth===================================
        fnd_global.enter_global_management(user=request.user, session=request.session)

    # 为了使process_response中的fnd_global.leave方法正常执行,
    # 这个函数只能抛出PermissionDenied或return一个Response.
    #def process_view(self, request):
    def process_view(self, request, view_func, view_args, view_kwargs):
        """
       将请求类型分成三类
       1,resp(protected),这类请求需要验证用户auth,和根据指定的resp_id,menu_id,function_id验证用户是否可以执行指定的程序.(fnd.site.resp)
         if not auth:
             raise django.NoPException     
         if not ResponsibilityCheck(resp_id, menu_id, function_id):
             raise django.NoPException
         fnd_global.set_resp_id(resp_id)
         fnd_global.set_menu_id(menu_id)
         fnd_golbal.set_function_id(function_id)
       2,user(protected),这类请求只需要验证用户auth,也就是说只要用户Login后,就可以访问.(fnd.site.user)
         if not auth:
             raise django.NoPException
       3,pub(public),这类请求是公共的,任何用户都可以访问,不需要Login.(fnd.site.root)   
        """
        try:
            # 使用mod_python时设定,context前缀
            context_prefix = request.django_root
            if context_prefix.endswith('/'):
                fnd_global.set_attr("context_prefix", context_prefix)
            else:
                fnd_global.set_attr("context_prefix", context_prefix + '/')
        except AttributeError:
            fnd_global.set_attr("context_prefix", '/')
        # 当前控制器前缀
        if view_kwargs.has_key('site_prefix'):
            fnd_global.set_attr("site_prefix", view_kwargs['site_prefix'])

        # 处理用户语言
        if not fnd_global.session.has_key('language'):
            fnd_global.session['language'] = request.META['HTTP_ACCEPT_LANGUAGE']

    def process_exception(self, request, exception):
        pass

    def process_response(self, request, response):
        # start session===============================
        """
        If request.session was modified, or if the configuration is to save the
        session every time, save the changes and set a session cookie.
        """
        try:
            accessed = request.session.accessed
            modified = request.session.modified
        except AttributeError:
            pass
        else:
            if accessed:
                patch_vary_headers(response, ('Cookie',))
            if modified or settings.SESSION_SAVE_EVERY_REQUEST:
                if request.session.get_expire_at_browser_close():
                    max_age = None
                    expires = None
                else:
                    max_age = request.session.get_expiry_age()
                    expires_time = time.time() + max_age
                    expires = cookie_date(expires_time)
                # Save the session data and refresh the client cookie.
                request.session.save()
                response.set_cookie(settings.SESSION_COOKIE_NAME,
                        request.session.session_key, max_age=max_age,
                        expires=expires, domain=settings.SESSION_COOKIE_DOMAIN,
                        path=settings.SESSION_COOKIE_PATH,
                        secure=settings.SESSION_COOKIE_SECURE or None)
        # end session=================================

        # ============================== 部缓存页面数据,也可以在apache中设定
        # Header set Pragma "no-cache"
        # Header set Cache-Control "no-cache"
        # Header set Expires "-1"

        response['Pragma'] = 'no-cache'
        response['Cache-Control'] = 'no-cache'
        response['Expires'] = '-1'


        fnd_global.leave_global_management()

        return response



