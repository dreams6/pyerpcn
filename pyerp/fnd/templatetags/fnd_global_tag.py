# -*- coding: utf-8 -*- 

from django.template import Library
from django.utils.safestring import mark_safe


from pyerp.fnd.gbl import fnd_global
from pyerp.fnd.utils.version import get_svn_revision, get_version

__svnid__ = '$Id$'
__svn__ = get_svn_revision(__name__)


register = Library()


def get_fnd_user():

    return fnd_global.user
get_fnd_user = register.simple_tag(get_fnd_user)

