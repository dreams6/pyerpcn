# -*- coding: utf-8 -*-
from pyerp.fnd.utils.version import get_svn_revision, get_version
__svnid__ = '$Id: __init__.py 54 2010-01-08 13:14:33Z yuhere $'
__svn__ = get_svn_revision(__name__)

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
