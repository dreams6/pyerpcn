# -*- coding: utf-8 -*- 

from django.conf.urls.defaults import *
from django.conf import settings

from pyerp.fnd.sites import respsite, usersite, pubsite, rootsite

urlpatterns = patterns('')

if settings.DEBUG:
    urlpatterns += patterns('',
        ('^' + settings.FND_MEDIA_PREFIX[1:] + '(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'd:/workspace1/ec/media', 'show_indexes': True}),
    )


urlpatterns += patterns('',
    ('^' + settings.FND_RESP_SITE_PREFIX  + '(?P<resp_id>\d+)/(?P<menu_id>\d+)/(?P<function_id>\d+)/(?P<url>.*)', respsite.root),
    ('^' + settings.FND_USER_SITE_PREFIX  + '(?P<url>.*)'                                                       , usersite.root),
    ('^' + settings.FND_PUB_SITE_PREFIX   + '(?P<url>.*)'                                                       , pubsite.root ),
    ('^(?P<url>.*)'                                                                                             , rootsite.root ),
)

if not settings.DEBUG:
    handler404 = 'pyerp.fnd.views.page_not_found'
    handler500 = 'pyerp.fnd.views.server_error'
