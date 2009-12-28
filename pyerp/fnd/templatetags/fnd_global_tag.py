# -*- coding: utf-8 -*- 

from django.template import Library
from django.utils.safestring import mark_safe


from pyerp.fnd.gbl import fnd_global


register = Library()


def get_fnd_user():

    return fnd_global.user
get_fnd_user = register.simple_tag(get_fnd_user)

