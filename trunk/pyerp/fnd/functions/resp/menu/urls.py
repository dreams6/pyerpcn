# -*- coding: utf-8 -*- 
from django.conf.urls.defaults import *
from django.conf import settings
from pyerp.fnd.utils.version import get_svn_revision, get_version

__svnid__ = '$Id$'
__svn__ = get_svn_revision(__name__)


urlpatterns = patterns('pyerp.fnd.functions.resp.menu.views',
    (r'^$'          , 'index'),
    (r'^add/$'                , 'add'),
    (r'^save/$'               , 'save'),
    (r'^submenu_sug/(?P<m_id>\d+)/$' , 'submenu_sug'),
    (r'^submenu_sug/$'               , 'submenu_sug'),
    (r'^func_sug/$'                  , 'func_sug'),
    (r'^(?P<f_id>\d+)/$'      , 'edit'),
)


