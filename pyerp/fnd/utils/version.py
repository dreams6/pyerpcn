# -*- coding: utf-8 -*- 

__svnid__ = '$Id$'

import re
import os

def get_svn_id(svnid=None, module=None):
    if module:
        path = os.path.dirname(module.__file__)
        root_mod_name = module.__name__
        src_root = os.path.dirname(path[:0-len(module.__name__)])
        for dirpath, dirnames, filenames in os.walk(path):
            # Ignore dirnames that start with '.'
            for i, dirname in enumerate(dirnames):
                if dirname.startswith('.'): 
                    del dirnames[i]
                else:
                    if os.path.exists(os.path.join(dirname, '__init__.py')):
                        del dirnames[i]
                        # mod = __import__(mod_path, {}, {}, [''])
                        # mod.get_version()

            for f in filenames:
                mod_path = None
                if f.endswith('.py') and '__init__.py' != f:
                    mod_path = root_mod_name + '.' + dirpath[len(path)+1:].replace(os.path.sep, '.')
                elif f.endswith('.py'):
                    mod_path = root_mod_name + '.' + dirpath[len(path)+1:].replace(os.path.sep, '.')
                    mod_path = mod_path + '.' + f[:-3]
                if mod_path:
                    #print mod_path
                    pass
                    # mod = __import__(mod_path, {}, {}, [''])
                    #print mod
                    #if mod and hasattr(mod, '__svnid__'):
                        # print mod.get_version()
    elif svnid:
        # bow for the mighty regular expression
        svnidrep = r'^\$Id: (?P<filename>.+) (?P<revision>\d+) (?P<last_changed_date>\d{4}-\d{2}-\d{1,2}) (?P<last_changed_time>\d{2}:\d{2}:\d{2})Z (?P<author>\w+.+) \$$'
        # parse the svn Id
        match_obj = re.match(svnidrep, svnid)
        if match_obj:
            return match_obj.group('revision', 'last_changed_date', 'author')
        else:
            return (None, None, None)
    else:
        return (None, None, None)

def get_svn_revision(path):
    """
    Returns the SVN last commit revision in the form SVN-XXXX,
    where XXXX is the revision number.

    Returns SVN-unknown if anything goes wrong, such as an unexpected
    format of internal SVN files.

    If path is provided, it should be a directory whose SVN info you want to
    inspect. If it's not provided, this will use the root django/ package
    directory.
    copy from django.utils.version packages.
    """
    import os.path
    rev = None
    if path is None:
        path = __path__[0]
    entries_path = '%s/.svn/entries' % path
    if os.path.exists(entries_path):
        entries = open(entries_path, 'r').readlines()
        #last_modifed_date entries[9].rstrip()
        rev = entries[10].rstrip()
        #author = entries[11].rstrip()
    if rev:
        return 'SVN-%s' % rev
    return 'SVN-unknown'

if __name__ == '__main__':
    print get_svn_id(__svnid__)

