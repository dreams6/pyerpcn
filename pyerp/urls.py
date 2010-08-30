# -*- coding: utf-8 -*- 

from django.conf.urls.defaults import patterns
from django.conf import settings

from pyerp.fnd.sites import respsite, usersite, pubsite, rootsite

urlpatterns = patterns('')

urlpatterns += patterns('',
    ('^' + settings.FND_RESP_SITE_PREFIX  + '(?P<resp_id>\d+)/(?P<menu_id>\d+)/(?P<function_id>\d+)/(?P<url>.*)', respsite.root),
    ('^' + settings.FND_USER_SITE_PREFIX  + '(?P<url>.*)'                                                       , usersite.root),
    ('^' + settings.FND_PUB_SITE_PREFIX   + '(?P<url>.*)'                                                       , pubsite.root ),
    ('^(?P<url>.*)'                                                                                             , rootsite.root ),
)

if not settings.DEBUG:
    handler404 = 'pyerp.fnd.views.page_not_found'
    handler500 = 'pyerp.fnd.views.server_error'
