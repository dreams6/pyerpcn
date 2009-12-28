# -*- coding: utf-8 -*- 


from pyerp.fnd.shortcuts import fnd_render_to_response


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
    return fnd_render_to_response('404.html', context)

def server_error(request, error_message='', extra_context=None):
    context = {
        'app_path': request.get_full_path(),
        'error_message': error_message,
    }
    context.update(extra_context or {})
    return fnd_render_to_response('500.html', context)