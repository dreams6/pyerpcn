# -*- coding: utf-8 -*- 

import urllib

from django.http import HttpResponseRedirect
from django.conf import settings

from pyerp.fnd.shortcuts import fnd_render_to_response
from pyerp.fnd.gbl import fnd_global
from pyerp.fnd import models as fnd_models
from pyerp.fnd.profile import fnd_profile


def display_main(request, func_id=None):
    
    fun = fnd_models.Function.objects.get(pk=func_id)
    req = urllib.urlencode({
          # "reporter"    : fnd_global.user.username,
          "summary"     : "",
          "type"        : "缺陷",
          "description" : "功能: %s \n\n"     \
                          "功能描述: %s \n\n" \
                          "版本: %s \n\n"     \
                          "模块: %s \n\n"     \
                          "问题描述: \n\n" % (
                           fun.name.encode("utf-8"), 
                           fun.description.encode("utf-8"),
                           fun.version, 
                           fun.package.encode("utf-8"),
                           ),
#          "action"      : "create",
#          "status"      : "new",
          "priority"    : "中等优先级",
          "milestone"   : "01_Pilot",
          "component"   : "fnd",
          "version"     : __import__('pyerp').get_version(),
          "keywords"    : "",
          "cc"          : ""
        })

    return HttpResponseRedirect("http://code.pyerp.cn/newticket?" + req)

