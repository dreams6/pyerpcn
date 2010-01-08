# -*- coding: utf-8 -*- 
from pyerp.fnd.utils.version import get_svn_revision, get_version
__svnid__ = '$Id: __init__.py 40 2010-01-06 14:04:43Z yuhere $'
__svn__ = get_svn_revision(__name__)

import unittest
from pyerp.fnd.management import fnd_init, fnd_init_currency, fnd_init_notice, fnd_init_concurrent

class ManagementTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass


    def test_fnd_init(self):
        fnd_init()
        self.assertEquals('1', '1')

    def test_fnd_init_currency(self):
        fnd_init_currency()
        self.assertEquals('1', '1')

    def test_fnd_init_notice(self):
        fnd_init_notice()
        self.assertEquals('1', '1')

    def test_fnd_init_concurrent(self):
        fnd_init_concurrent()
        self.assertEquals('1', '1')

