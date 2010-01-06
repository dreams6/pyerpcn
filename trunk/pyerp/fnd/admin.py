# -*- coding: utf-8 -*- 

from django.contrib import admin
from pyerp.fnd.models import *
from pyerp.fnd.utils.version import get_svn_revision, get_version

__svnid__ = '$Id$'
__svn__ = get_svn_revision(__name__)


admin.site.register(LookUpNode)
admin.site.register(MessageResource)
admin.site.register(ValueSet)

admin.site.register(KeyFlexField)
admin.site.register(KeyFlexFieldSegment)
admin.site.register(ProfileOption)
admin.site.register(ProfileOptionValues)
admin.site.register(Function)
admin.site.register(Menu)
admin.site.register(MenuItem)
admin.site.register(Responsibility)

admin.site.register(User)
admin.site.register(UserResp)

admin.site.register(Session)


