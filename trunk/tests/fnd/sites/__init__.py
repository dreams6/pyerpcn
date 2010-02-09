# -*- coding: utf-8 -*-
__svnid__ = '$Id: __init__.py 91 2010-01-31 04:14:47Z yuhere $'

import unittest
from django.test.client import Client
from django.conf import settings


class MediaTestCase(unittest.TestCase):

    def setUp(self):
        pass
    
    def tearDown(self):
        pass

    def test_image(self):
        c = Client()
        response = c.get('' + settings.FND_MEDIA_PREFIX + 'images/pyerp.ico')
        self.assertEquals(200, response.status_code)


