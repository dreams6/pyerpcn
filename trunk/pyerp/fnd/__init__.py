# -*- coding: utf-8 -*- 

import sys

VERSION = (0, 0, 1, 'dev', 0)

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

    return version

def sss():
    from pyerp.fnd.utils.version import get_svn_id
    print get_svn_id(module=sys.modules[__name__])
    
    
