# -*- coding: utf-8 -*- 
import urllib

from django.http import HttpResponseRedirect
from django.conf import settings

from pyerp.fnd.shortcuts import fnd_render_to_response
from pyerp.fnd.gbl import fnd_global
from pyerp.fnd import models as fnd_models
from pyerp.fnd.profile import fnd_profile
from pyerp.fnd.utils.version import get_svn_revision, get_version

__svnid__ = '$Id$'
__svn__ = get_svn_revision(__name__)


def display_main(request, func_id=None):
    fun = fnd_models.Function.objects.get(pk=func_id)
    referer = urllib.urlencode({
          # "reporter"    : fnd_global.user.username,
          "summary"     : "",
          "type"        : "缺陷",
          "description" : "功能: %s \n\n"        \
                          "功能描述: %s \n\n"    \
                          "版本: %s \n\n"        \
                          "模块: %s \n\n"        \
                          "客户端环境: %s \n\n"  \
                          "客户端IP: %s \n\n"    \
                          "问题描述: \n\n" % (
                           fun.name.encode("utf-8"), 
                           fun.description.encode("utf-8"),
                           fun.version, 
                           fun.package.encode("utf-8"),
                           request.META['HTTP_USER_AGENT'],
                           request.META['REMOTE_ADDR'],
                           ),
#          "action"      : "create",
#          "status"      : "new",
          "priority"    : "中等优先级",
          "milestone"   : "01_Pilot",
          "component"   : "fnd",
          "version"     : __import__('pyerp').__version__,
          "keywords"    : "",
          "cc"          : fun.svn_revision[2]  # SVN's author
        })

    support_site_url = hasattr(settings, 'SUPPORT_SITE_URL') and settings.SUPPORT_SITE_URL or 'http://code.pyerp.cn'
    req = urllib.urlencode({
          'sn'       : settings.SUPPORT_SN,
          'referer'  : support_site_url + '/newticket?' + referer
        })

    return HttpResponseRedirect(support_site_url + '/snlogin?' + req)

