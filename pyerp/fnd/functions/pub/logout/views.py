# -*- coding: utf-8 -*- 


from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.conf import settings

from pyerp.fnd.shortcuts import fnd_render_to_response
from pyerp.fnd.gbl import fnd_global


def do_logout(request, next_page=None):
    "Logs out the user and displays 'You are logged out' message."
    from pyerp.fnd.auth import logout
    logout(request)
    if next_page is None:
        return HttpResponseRedirect(fnd_global.context_prefix + fnd_global.site_prefix)
    else:
        # Redirect to this page until the session has been cleared.
        return HttpResponseRedirect(next_page)

def logout(request):
    return do_logout(request)


