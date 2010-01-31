# -*- coding: utf-8 -*-
__svnid__ = '$Id$'

import unittest
from django.test.client import Client
from django.conf import settings


class ChangePwdTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_show_index(self):
        c = Client()
        c.login(username='u0', password='test')
        response = c.get('/' + settings.FND_USER_SITE_PREFIX + 'changepwd/')
        self.assertEquals(200, response.status_code)

