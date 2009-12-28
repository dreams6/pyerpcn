# -*- coding: utf-8 -*- 

from django.conf.urls.defaults import *
from django.conf import settings


urlpatterns = patterns('pyerp.fnd.functions.resp.executable.views',
    (r'^$'          , 'index'),
    (r'^load/$'     , 'index_load'),
    
)


