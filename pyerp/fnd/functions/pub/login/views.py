# -*- coding: utf-8 -*- 

from django.conf import settings

from pyerp.fnd.shortcuts import fnd_render_to_response
from pyerp.fnd.gbl import fnd_global


def display_login_form(request, error_message='', app_path=None, extra_context=None):
    request.session.set_test_cookie()
    context = {
        'app_path': app_path or request.get_full_path(),
        'error_message': error_message,
    }
    context.update(extra_context or {})
    return fnd_render_to_response('pub/login/login.html', context)


def login(request):
    
    return display_login_form(request, 
                              '', 
                              fnd_global.context_prefix + settings.FND_USER_SITE_PREFIX + 'main/')

