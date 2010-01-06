# -*- coding: utf-8 -*-
from pyerp.fnd.utils.version import get_svn_revision, get_version

__svnid__ = '$Id$'
__svn__ = get_svn_revision(__name__)
__version__ = get_version(0, 0, 1, 'dev', 0, __svn__[0])
