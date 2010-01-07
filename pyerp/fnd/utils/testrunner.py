# -*- coding: utf-8 -*-


from bitten.util.testrunner import unittest as b_unittest



class pyerpunittest(b_unittest):
    
    description = b_unittest.description + ', and setup Django unittest evn'
    
    """
    add follow info into setup.py's setup() option
    entry_points = {
        'distutils.commands': [
            'pyerpunittest = pyerp.fnd.utils.testrunner:pyerpunittest'
        ],
    and run python setup.py egg_info first.(setuptools is required)
    about django testing: django.test.simple
    """
    # TODO: define option Django's setting
    user_options = b_unittest.user_options + [
        ('django-settings=', None, "Django settings module"),
    ]
    
    
    def initialize_options(self):
        b_unittest.initialize_options(self)
        self.django_settings = 'tests.settings'

    def finalize_options(self):
        b_unittest.finalize_options(self)

    def run_tests(self):

        import os
        os.environ['DJANGO_SETTINGS_MODULE'] = self.django_settings

        from django.test.utils import setup_test_environment, teardown_test_environment
        from django.conf import settings

        setup_test_environment()
        settings.DEBUG = False

        old_name = settings.DATABASE_NAME
        from django.db import connection
        connection.creation.create_test_db(1, autoclobber=False)
        # execute test suites
        b_unittest.run_tests(self)

        connection.creation.destroy_test_db(old_name, 1)
        teardown_test_environment()

