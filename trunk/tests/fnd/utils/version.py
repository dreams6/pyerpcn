# -*- coding: utf-8 -*- 
__svnid__ = '$Id$'

import unittest

class VersionTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_parse_svn_id(self):
        from pyerp.fnd.utils import version
        _svn = version._parse_svn_id('$Id$')
        self.assertNotEqual(_svn[0], None)
        self.assertEqual(len(_svn), 3)
        
        _svn = version._parse_svn_id('')
        self.assertEqual(_svn[0], None)
        self.assertEqual(len(_svn), 3)

    def test_get_version(self):
        from pyerp.fnd.utils import version
        ver = version.get_version(0, 0, 1, 'alpha', ('9', '2010-01-08', 'yu.peng'))
        self.assertEquals('0.0.1-alpha-r9', ver)
        ver = version.get_version(0, 0, 1, 'final', ('10', '2010-01-08', 'yu.peng'))
        self.assertEquals('0.0.1-final', ver)
        ver = version.get_version(0, 0, 1, 'release', ('30', '2010-01-08', 'yu.peng'))
        self.assertEquals('0.0.1-r30', ver)

    def test_get_svn_revision(self):
        from pyerp.fnd.utils import version
        _svn_ = version.get_svn_revision(__name__)
        self.assertEquals(len(_svn_), 3)
        from tests.fnd import utils
        _svn_ = version.get_svn_revision(utils.__name__)
        self.assertEquals(len(_svn_), 3)

