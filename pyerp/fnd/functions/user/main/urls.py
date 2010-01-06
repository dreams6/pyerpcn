# -*- coding: utf-8 -*- 
from django.conf.urls.defaults import *
from pyerp.fnd.utils.version import get_svn_revision, get_version

__svnid__ = '$Id$'
__svn__ = get_svn_revision(__name__)


urlpatterns = patterns('pyerp.fnd.functions.user.main.views',
    # (r'^/$'    , 'display_main'),
    (r'^(?P<resp_id>\d+)/$'    , 'display_main'),
    (r'^$'                    , 'display_main'),
)

