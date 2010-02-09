# -*- coding: utf-8 -*- 

"""
这个模块实现了用户管理相关功能。

create_user() 用于创建用户。
为指定用户绑定职责。
"""

from datetime import datetime, date

from pyerp.fnd import models
from pyerp.fnd.gbl import fnd_global
from pyerp.fnd.utils.version import get_svn_revision, get_version

__svnid__ = '$Id: user.py 98 2010-02-01 13:52:36Z yuhere $'
__svn__ = get_svn_revision(__name__)


def create_user(username, password, description, email, 
                pwd_expiration_type=0, pwd_lifespan=0, 
                start_date_active=date.today(), end_date_active=None):
    user = models.User()
    user.username    = username
    user.set_password(password)
    user.description = description
    user.email       = email
    user.fax         = None
    user.pwd_expiration_type    = pwd_expiration_type   # 0:none 1:days 2:accesses
    user.pwd_lifespan  = pwd_lifespan
    user.start_date_active = start_date_active
    user.end_date_active = end_date_active
    user.save()
    return user

