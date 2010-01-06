# -*- coding: utf-8 -*-

import unittest


class FirstTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_first(self):
        import pyerp
        print pyerp.__version__
        self.assertEquals('1', '1')


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(FirstTestCase, 'test'))
    from tests.fnd.utils import version
    suite.addTest(unittest.makeSuite(version.VersionTestCase, 'test'))
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='suite')
