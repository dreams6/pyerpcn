# -*- coding: utf-8 -*- 

from pyerp.fnd.utils.version import get_svn_revision, get_version

__svnid__ = '$Id$'
__svn__ = get_svn_revision(__name__)
__version__ = get_version(0, 1, 0, 'alpha', __svn__)

