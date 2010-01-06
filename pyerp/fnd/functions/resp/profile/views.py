# -*- coding: utf-8 -*- 
from pyerp.fnd.shortcuts import fnd_render_to_response
from pyerp.fnd.utils.version import get_svn_revision, get_version

__svnid__ = '$Id$'
__svn__ = get_svn_revision(__name__)


def system_profile(request):
    context = {
        'app_path': request.get_full_path(),
    }
    return fnd_render_to_response('resp/profile/index.html', context)


def person_profile(request):
    context = {
        'app_path': request.get_full_path(),
    }
    return fnd_render_to_response('resp/profile/index.html', context)

