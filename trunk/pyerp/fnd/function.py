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

from pyerp.fnd.gbl import fnd_global


import models

def add(name, description, package, paramters):
  fun = models.Function()
  fun.name = name
  fun.description = description
  fun.package = package
  fun.paramters = paramters
  # ==============================
  fun.created_by = fnd_global.user_id
  fun.last_updated_by = fnd_global.user_id
  # ==============================
  fun.save()
  return fun

def remove():
  pass
  

