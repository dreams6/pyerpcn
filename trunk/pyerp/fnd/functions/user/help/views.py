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
    support_site_url = hasattr(settings, 'SUPPORT_SITE_URL') and settings.SUPPORT_SITE_URL or 'http://code.pyerp.cn'
    return HttpResponseRedirect(support_site_url + '/wiki/help/' + fun.package.encode("utf-8"))

