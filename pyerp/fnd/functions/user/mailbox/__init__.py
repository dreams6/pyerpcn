# -*- coding: utf-8 -*- 

VERSION = (0, 0, 2, 'dev', 0)

def get_version():
    version = '%s.%s' % (VERSION[0], VERSION[1])
    if VERSION[2]:
        version = '%s.%s' % (version, VERSION[2])
    if VERSION[3:] == ('alpha', 0):
        version = '%s pre-alpha' % version
    else:
        version = '%s %s' % (version, VERSION[3])
        if VERSION[3] != 'final':
            version = '%s %s' % (version, VERSION[4])
    from pyerp.fnd.utils.version import get_svn_revision
    svn_rev = get_svn_revision(__path__[0])
    if svn_rev != 'SVN-unknown':
        version = "%s %s" % (version, svn_rev)
    return version

