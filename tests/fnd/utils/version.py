# -*- coding: utf-8 -*- 

import unittest

class VersionTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_version(self):
        from pyerp.fnd.utils import version
        ver = version.get_version(0, 0, 1, 'dev', 0)
        self.assertEquals('0.0.1-dev-0', ver)




