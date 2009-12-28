# -*- coding: utf-8 -*- 

from django.conf.urls.defaults import *
from django.conf import settings


urlpatterns = patterns('pyerp.fnd.functions.resp.function.views',
    (r'^$'                    , 'index'),
    (r'^add/$'                , 'add'),
    (r'^(?P<f_id>\d+)/$'      , 'edit'),
    (r'^func_sug/$'           , 'func_sug'),
)


