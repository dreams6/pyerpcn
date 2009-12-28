# -*- coding: utf-8 -*- 

from django.conf.urls.defaults import *
from django.conf import settings


urlpatterns = patterns('pyerp.fnd.functions.resp.profile.views',
    (r'^system/$'          , 'system_profile'),
    (r'^person/$'          , 'person_profile'),
    
)


