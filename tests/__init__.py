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
    from tests.fnd import management
    suite.addTest(unittest.makeSuite(management.ManagementTestCase, 'test'))
    from tests.fnd.functions.pub import login
    suite.addTest(unittest.makeSuite(login.LoginTestCase, 'test'))

    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='suite')
