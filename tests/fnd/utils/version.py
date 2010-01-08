# -*- coding: utf-8 -*- 

import unittest

__svnid__ = '$Id$'

class VersionTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_version(self):
        from pyerp.fnd.utils import version
        ver = version.get_version(0, 0, 1, 'alpha', 0)
        self.assertEquals('0.0.1-pre-alpha', ver)
        ver = version.get_version(0, 0, 1, 'final', 0)
        self.assertEquals('0.0.1-final', ver)
        ver = version.get_version(0, 0, 1, 'dev', 0)
        self.assertEquals('0.0.1-dev-0', ver)

    def test_get_svn_revision(self):
        from pyerp.fnd.utils import version
        _svn_ = version.get_svn_revision(__name__)
        self.assertEquals(len(_svn_), 3)
        from tests.fnd import utils
        _svn_ = version.get_svn_revision(utils.__name__)
        print _svn_
        self.assertEquals(len(_svn_), 3)
        
        


