# -*- coding: utf-8 -*-
__svnid__ = '$Id$'

import unittest
from django.test.client import Client
from django.conf import settings


class IndexTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_show_index(self):
        c = Client()
        response = c.get('/' + settings.FND_PUB_SITE_PREFIX + '/')
        self.assertEquals(200, response.status_code)

