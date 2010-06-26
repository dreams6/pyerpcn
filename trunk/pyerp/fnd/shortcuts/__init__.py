# -*- coding: utf-8 -*- 

from django.shortcuts import render_to_response
from django.conf import settings
from django.template import RequestContext
from django import template, templatetags

from pyerp.fnd.gbl import fnd_global
from pyerp.fnd.profile import fnd_profile
from pyerp.fnd.utils.version import get_svn_revision, get_version

__svnid__ = '$Id$'
__svn__ = get_svn_revision(__name__)


#
#
#
def fnd_render_to_response(template_name, extra_context=None, request=None):
    context = {
        'fnd_global': fnd_global,
        'fnd_profile': fnd_profile,
        'fnd_media_prefix': fnd_global.context_prefix + settings.FND_MEDIA_PREFIX,
        'fnd_resp_site_prefix': fnd_global.context_prefix + settings.FND_RESP_SITE_PREFIX,
        'fnd_user_site_prefix': fnd_global.context_prefix + settings.FND_USER_SITE_PREFIX,
        'fnd_pub_site_prefix':  fnd_global.context_prefix + settings.FND_PUB_SITE_PREFIX,
        'fnd_resp_path' :  fnd_global.resp_id!=-1 and str(fnd_global.resp_id) + '/' + str(fnd_global.menu_id) + '/' + str(fnd_global.function_id) + '/' or ''
    }
    context.update(extra_context or {})
    ci = request and RequestContext(request)
    return render_to_response(template_name, context, context_instance=ci)

