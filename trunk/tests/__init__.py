# -*- coding: utf-8 -*-

import unittest


class FirstTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_first(self):
        import pyerp
        print pyerp.get_version()
        self.assertEquals('1', '1')


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(FirstTestCase, 'test'))
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='suite')
