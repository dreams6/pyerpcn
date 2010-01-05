# -*- coding: utf-8 -*- 

__svnid__ = '$Id:$'

import re

def get_svn_id(_svnid):
    # bow for the mighty regular expression
    svnidrep = r'^\$Id: (?P<filename>.+) (?P<revision>\d+) (?P<last_changed_date>\d{4}-\d{2}-\d{1,2}) (?P<last_changed_time>\d{2}:\d{2}:\d{2})Z (?P<author>\w+.+) \$$'
    # parse the svn Id
    return  re.match(svnidrep, _svnid).group('last_changed_date', 'author')

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
