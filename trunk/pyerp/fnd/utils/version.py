# -*- coding: utf-8 -*- 

import os, sys
import re

def _parse_svn_id(_svnid):
    # bow for the mighty regular expression
    svnidrep = r'^\$Id: (?P<filename>.+) (?P<revision>\d+) (?P<last_changed_date>\d{4}-\d{2}-\d{1,2}) (?P<last_changed_time>\d{2}:\d{2}:\d{2})Z (?P<author>\w+.+) \$$'
    # parse the svn Id
    match_obj = re.match(svnidrep, _svnid)
    if match_obj:
        return match_obj.group('revision', 'last_changed_date', 'author')
    else:
        return (None, None, None)

def get_svn_revision(m__name__):
    mod = sys.modules[m__name__]
    m__file__ = mod.__file__
    svn_ret = (None, None, None)
    if hasattr(mod, '__svnid__'):
        svn_ret = _parse_svn_id(mod.__svnid__)
    
    if m__file__.endswith('__init__.py') or m__file__.endswith('__init__.pyc'):
        m__dir__ = os.path.dirname(m__file__)
        for f in os.listdir(m__dir__):
            if not f.startswith('.'):
                
                sub_name = None
                if os.path.isfile(os.path.join(m__dir__, f)):
                    if f.endswith('.py') and f != '__init__.py':
                        sub_name = m__name__ + '.' + f[:-3]
                elif os.path.isdir(os.path.join(m__dir__, f)):
                    sub_name = m__name__ + '.' + f
 
                if sub_name:
                    try:
                        sub_mod = __import__(sub_name, {}, {}, [''])
                        svn_sub_mod = (None, None, None)
                        if hasattr(sub_mod, '__svn__'):
                            svn_sub_mod = sub_mod.__svn__
                        svn_ret_rev = svn_ret[0] and int(svn_ret[0]) or 0
                        svn_sub_mod_rev = svn_sub_mod[0] and int(svn_sub_mod[0]) or 0
                        if svn_sub_mod_rev > svn_ret_rev:
                            svn_ret = svn_sub_mod
                    except:
                        pass
    return svn_ret

def get_version(*args):
    version = '%s.%s.%s' % args[:3] 
    if args[3] != 'release':
        version = '%s-%s' % (version, args[3]) 
    if args[3] != 'final': 
        if len(args)>4 and args[4]:
            version = "%s-r%s" % (version, args[4][0])
    return version

__svnid__ = '$Id$'
__svn__ = get_svn_revision(__name__)
