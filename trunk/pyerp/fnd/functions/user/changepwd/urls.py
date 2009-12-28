# -*- coding: utf-8 -*- 

from django.conf.urls.defaults import *


urlpatterns = patterns('pyerp.fnd.functions.user.changepwd.views',
    (r'^$'                    , 'display_main'),
)


