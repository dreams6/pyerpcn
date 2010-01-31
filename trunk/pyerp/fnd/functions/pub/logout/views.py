# -*- coding: utf-8 -*- 


from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.conf import settings

from pyerp.fnd.shortcuts import fnd_render_to_response
from pyerp.fnd.gbl import fnd_global
from pyerp.fnd.utils.version import get_svn_revision, get_version

__svnid__ = '$Id$'
__svn__ = get_svn_revision(__name__)


def do_logout(request):
    "Logs out the user and displays 'You are logged out' message."
    from pyerp.fnd.auth import logout
    logout(request)
    return HttpResponseRedirect(fnd_global.context_prefix + fnd_global.site_prefix)

def logout(request):
    return do_logout(request)


