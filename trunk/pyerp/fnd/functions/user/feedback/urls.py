# -*- coding: utf-8 -*- 

from django.conf.urls.defaults import *


urlpatterns = patterns('pyerp.fnd.functions.user.feedback.views',
    # (r'^/$'    , 'display_main'),
    (r'^(?P<func_id>\d+)/$'    , 'display_main'),
)

