# -*- coding: utf-8 -*-
__svnid__ = '$Id$'

import unittest
from django.test.client import Client
from django.conf import settings


class MailboxTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_show_inbox(self):
        c = Client()
        c.login(username='u0', password='test')
        response = c.get('/' + settings.FND_USER_SITE_PREFIX + 'mailbox/inbox/')
        self.assertEquals(200, response.status_code)

