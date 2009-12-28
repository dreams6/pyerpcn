# -*- coding: utf-8 -*- 

from pyerp.fnd.shortcuts import fnd_render_to_response


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

