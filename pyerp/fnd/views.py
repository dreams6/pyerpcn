# -*- coding: utf-8 -*- 

from django.http import HttpResponseNotFound

from pyerp.fnd.shortcuts import fnd_render_to_response
from pyerp.fnd.utils.version import get_svn_revision, get_version

__svnid__ = '$Id$'
__svn__ = get_svn_revision(__name__)


def display_http_403(request, error_message='', extra_context=None):
    context = {
        'app_path': request.get_full_path(),
        'error_message': error_message,
    }
    context.update(extra_context or {})
    return fnd_render_to_response('403.html', context)

def page_not_found(request, error_message='', extra_context=None):
    context = {
        'app_path': request.get_full_path(),
        'error_message': error_message,
    }
    context.update(extra_context or {})
    t = loader.get_template('404.html')  # You need to create a 404.html template.
    return http.HttpResponseNotFound(t.render(RequestContext(request, context)))
    # return fnd_render_to_response('404.html', context)

def server_error(request, error_message='', extra_context=None):
    context = {
        'app_path': request.get_full_path(),
        'error_message': error_message,
    }
    context.update(extra_context or {})
    return fnd_render_to_response('500.html', context)
