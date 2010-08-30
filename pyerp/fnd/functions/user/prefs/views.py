# -*- coding: utf-8 -*- 
from django.http import HttpResponseRedirect
from django.conf import settings
from django.views.i18n import set_language

from pyerp.fnd.shortcuts import fnd_render_to_response
from pyerp.fnd.gbl import fnd_global
from pyerp.fnd.profile import fnd_profile
from pyerp.fnd.utils.version import get_svn_revision, get_version
from pyerp.fnd.models import MailBox

__svnid__ = '$Id$'
__svn__ = get_svn_revision(__name__)


def display_main(request, resp_id=None):
    if request.method == 'POST':
        return set_language(request)
    else:
        supported_langs = settings.LANGUAGES
        context = {
            'app_path': request.get_full_path(),
            'resp_id': resp_id,
            'last_login': request.session.pop('last_login', None),  # 取出最后登录时间,显示在画面上
            'supported_languages' : supported_langs,
        }
        return fnd_render_to_response('user/prefs/index.html', context, request)


