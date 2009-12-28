# -*- coding: utf-8 -*- 

from django.conf.urls.defaults import *


urlpatterns = patterns('pyerp.fnd.functions.user.main.views',
    # (r'^/$'    , 'display_main'),
    (r'^(?P<resp_id>\d+)/$'    , 'display_main'),
    (r'^$'                    , 'display_main'),
)

