# -*- coding: utf-8 -*- 
__svnid__ = '$Id$'

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

