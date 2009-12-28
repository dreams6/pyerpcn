# -*- coding: utf-8 -*- 

from django.conf import settings

from pyerp.fnd.shortcuts import fnd_render_to_response
from pyerp.fnd.gbl import fnd_global



def index(request):
    context = {
        'app_path': request.get_full_path(),
    }
    return fnd_render_to_response('pub/index/index.html', context)

