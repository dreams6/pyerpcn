# -*- coding: utf-8 -*- 

import time

from django.conf import settings
from pyerp.fnd.gbl import fnd_global
from pyerp.fnd.utils.version import get_svn_revision, get_version

__svnid__ = '$Id$'
__svn__ = get_svn_revision(__name__)


class FndGlobalMiddleware(object):

    def process_request(self, request):
        """
         1, 处理session
         2, 处理auth
         3, 初始化fnd_global
        """
        # start auth=================================
        # request.__class__.user = LazyUser()
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
        fnd_global.leave_global_management()
        return response


class FndMediaMiddleware(object):

        
    def process_view(self, request, view_func, view_args, view_kwargs):
        # if metch of media's url return the media
        request_path_info = request.path_info
        if request_path_info.startswith(settings.FND_MEDIA_PREFIX):
            from pyerp.fnd.sites import mediasite
            return mediasite.root(request, request_path_info[len(settings.FND_MEDIA_PREFIX):])

    def process_response(self, request, response):
        # fix response header when request a media file.
        request_path_info = request.path_info
        if request_path_info.startswith(settings.FND_MEDIA_PREFIX):
            if 'Vary' in response:
                del response['Vary']
            pass # fix header
        return response

