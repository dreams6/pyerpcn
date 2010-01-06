# -*- coding: utf-8 -*- 

from django.conf.urls.defaults import *
from django.conf import settings

from pyerp.fnd import models as fnd_models
from pyerp.fnd.utils.version import get_svn_revision, get_version

__svnid__ = '$Id$'
__svn__ = get_svn_revision(__name__)


urlpatterns = patterns('')

# 这里只会被执行一次, TODO 加载所有已经安装的APPS下的functions.user.urls
fmlist = fnd_models.FuncMapping.objects.filter(type='user').order_by('seq')
for fm in fmlist:
    urlpatterns += patterns('',
        (fm.regex_pattern, include(fm.function.urlconf), {'func': fm.function}),
    )

