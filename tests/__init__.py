# -*- coding: utf-8 -*-
__svnid__ = '$Id$'

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
    from tests.fnd.functions.pub import index
    suite.addTest(unittest.makeSuite(index.IndexTestCase, 'test'))
    
    from tests.fnd.functions.user import main
    suite.addTest(unittest.makeSuite(main.MainTestCase, 'test'))
    from tests.fnd.functions.user import mailbox
    suite.addTest(unittest.makeSuite(mailbox.MailboxTestCase, 'test'))
    from tests.fnd.functions.user import changepwd
    suite.addTest(unittest.makeSuite(changepwd.ChangePwdTestCase, 'test'))

    from tests.fnd.functions.resp import executable
    suite.addTest(unittest.makeSuite(executable.ExecutableTestCase, 'test'))
    from tests.fnd.functions.resp import menu
    suite.addTest(unittest.makeSuite(menu.MenuTestCase, 'test'))
    from tests.fnd.functions.resp import profile
    suite.addTest(unittest.makeSuite(profile.ProfileTestCase, 'test'))
    from tests.fnd import sites
    suite.addTest(unittest.makeSuite(sites.MediaTestCase, 'test'))
    
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='suite')
