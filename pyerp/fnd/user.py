# -*- coding: utf-8 -*- 

"""
This module implements a transaction manager that can be used to define
transaction handling in a request or view function. It is used by transaction
control middleware and decorators.

The transaction manager can be in managed or in auto state. Auto state means the
system is using a commit-on-save strategy (actually it's more like
commit-on-change). As soon as the .save() or .delete() (or related) methods are
called, a commit is made.

Managed transactions don't do those commits, but will need some kind of manual
or implicit commits or rollbacks.
"""

from datetime import datetime, date

from pyerp.fnd import models
from pyerp.fnd.gbl import fnd_global
from pyerp.fnd.utils.version import get_svn_revision, get_version

__svnid__ = '$Id$'
__svn__ = get_svn_revision(__name__)



def get_md5_hexdigest(raw_password):
    """
    Returns a string of the hexdigest of the given plaintext password and salt
    using the given algorithm ('md5', 'sha1' or 'crypt').
    """
    try:
        import hashlib
    except ImportError:
        import md5
        return md5.new(raw_password).hexdigest()
    else:
        return hashlib.md5(raw_password).hexdigest()
    raise ValueError("Got unknown password algorithm type in password.")


def add(username, password, description, email, pwd_expiration_type=0, pwd_lifespan=0, start_date_active=date.today(), end_date_active=None):
    user = models.User()
    user.username    = username
    user.first_name = "first_name"
    user.last_name = "last_name"
    user.password    = get_md5_hexdigest(password)         # ????
    user.description = description
    user.email       = email
    user.fax         = None
    user.pwd_expiration_type    = pwd_expiration_type   # 0:none 1:days 2:accesses
    user.pwd_lifespan  = pwd_lifespan
    user.start_date_active = start_date_active
    user.end_date_active = end_date_active
    # ==============================
    user.created_by = fnd_global.user_id
    user.last_updated_by = fnd_global.user_id
    # ==============================
    user.save()
    return user

def addresp(user, resp, description):
    user.responsibilities.add(resp)
