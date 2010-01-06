# -*- coding: utf-8 -*- 
from django.http import HttpResponseRedirect
from django.conf import settings

from pyerp.fnd.shortcuts import fnd_render_to_response
from pyerp.fnd.gbl import fnd_global
from pyerp.fnd.profile import fnd_profile
from pyerp.fnd.utils.version import get_svn_revision, get_version

__svnid__ = '$Id$'
__svn__ = get_svn_revision(__name__)



def display_main(request, resp_id=None):
    # 判断用户是否设定了缺省主页
    user_home_page = fnd_profile['user_home_page']
    if user_home_page:
        return HttpResponseRedirect(fnd_global.context_prefix + settings.FND_USER_SITE_PREFIX + user_home_page)
    
    context = {
        'app_path': request.get_full_path(),
        'resp_id': resp_id,
        'last_login': request.session.pop('last_login', None),  # 取出最后登录时间,显示在画面上
    }
    return fnd_render_to_response('user/main/index.html', context, request)


