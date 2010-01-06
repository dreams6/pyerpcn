# -*- coding: utf-8 -*- 

import unittest

__svnid__ = '$Id: __init__.py 45 2010-01-06 14:35:30Z yuhere $'

class VersionTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_version(self):
        from pyerp.fnd.utils import version
        ver = version.get_version(0, 0, 1, 'dev', 0)
        self.assertEquals('0.0.1-dev-0', ver)

    def test_get_svn_revision(self):
        from pyerp.fnd.utils import version
        _svn_ = version.get_svn_revision(__name__)
        self.assertEquals(len(_svn_), 3)


