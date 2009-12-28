# -*- coding: utf-8 -*- 

from pyerp.fnd.shortcuts import fnd_render_to_response

def index(request):
    context = {
        'app_path': request.get_full_path(),
    }
    return fnd_render_to_response('resp/user/index.html', context)

