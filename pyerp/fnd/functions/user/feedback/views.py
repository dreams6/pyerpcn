# -*- coding: utf-8 -*- 


from django.http import HttpResponseRedirect
from django.conf import settings

from pyerp.fnd.shortcuts import fnd_render_to_response
from pyerp.fnd.gbl import fnd_global
from pyerp.fnd import models as fnd_models
from pyerp.fnd.profile import fnd_profile
import urllib


def display_main(request, func_id=None):
    # 判断用户是否设定了缺省主页
    fun = fnd_models.Function.objects.get(pk=func_id)

    req = urllib.urlencode({"reporter"    : fnd_global.user.username,
          "summary"     : "",
          "type"        : "enhancement",
          "description" : """功能: %s \n
功能描述: %s \n
版本: %s \n
模块: %s \n
问题描述: \n""" % (fun.name.encode("utf-8"), 
                fun.package.encode("utf-8"),
                fun.description.encode("utf-8"), 
                fun.version),
#          "action"      : "create",
#          "status"      : "new",
          "priority"    : "major",
          "milestone"   : "NW-Django【Pilot】",
          "component"   : "NW-Django",
          "version"     : "1.0",
          "keywords"    : "",
          "cc"          : ""
        })
    
#    from pyerp.fnd.api import request as fnd_request
#    fnd_request.submit_request(1)
    
    return HttpResponseRedirect("https://ora12.gicp.net/trac/newticket?" + req)
    #return fnd_render_to_response('user/feedback/index.html', context, request)


