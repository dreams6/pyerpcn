# -*- coding: utf-8 -*-
__svnid__ = '$Id$'

import unittest
from django.test.client import Client
from django.conf import settings


class LoginTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_show_login(self):
        c = Client()
        response = c.get('/' + settings.FND_PUB_SITE_PREFIX + 'login/')
        self.assertEquals(200, response.status_code)

    def test_login(self):
        c = Client()
        c.login(username='u0', password='test')
        response = c.get('/' + settings.FND_USER_SITE_PREFIX + 'main/')
        self.assertEquals(200, response.status_code)

    def test_logout(self):
        c = Client()
        c.login(username='u0', password='test')
        response = c.get('/' + settings.FND_PUB_SITE_PREFIX + 'logout/')
        self.assertEquals(302, response.status_code)

