# -*- coding: utf-8 -*-
__svnid__ = '$Id$'

import unittest
from django.test.client import Client
from django.conf import settings

from pyerp.fnd import models as fnd_models
from pyerp.fnd.gbl import fnd_global
from pyerp.fnd.api import user as fnd_user

class ExecutableTestCase(unittest.TestCase):

    def setUp(self):
        fnd_global.enter_global_management(1)
        fun = fnd_models.Function()
        fun.name = 'test'
        fun.description = 'test'
        fun.package = 'pyerp.fnd.functions.resp.executable'
        fun.paramters = None
        fun.save()

        menu = fnd_models.Menu()
        menu.name = 'test'
        menu.description = 'test'
        menu.save()

        menuitem = fnd_models.MenuItem()
        menuitem.p_menu = menu
        menuitem.seq = 1
        menuitem.prompt = 'test'
        menuitem.description = 'test'
        menuitem.submenu = None
        menuitem.function = fun
        menuitem.save()

        resp = fnd_models.Responsibility()
        resp.name = 'test'
        resp.description = 'test'
        resp.menu = menu
        resp.save()

        test_user = fnd_user.create_user('ut_user', 'test', 'Pyerp Unit Test User', 'pyerp_test@yahoo.cn')
        test_user.responsibilities.add(resp)

        self._resp_path = str(resp.id) + '/' + str(menuitem.id) + '/' + str(fun.id) + '/' 

        fnd_global.leave_global_management()

    def tearDown(self):
        pass

    def test_show_index(self):
        c = Client()
        c.login(username='ut_user', password='test')
        response = c.get('/' + self._resp_path)
        self.assertEquals(200, response.status_code)

