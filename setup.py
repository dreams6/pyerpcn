# -*- coding: utf-8 -*- 

from setuptools import setup, find_packages
import os
import sys


import __builtin__
import sys
class RollbackImporter:
    def __init__(self):
        "Creates an instance and installs as the global importer"
        self.previousModules = sys.modules.copy()
        self.realImport = __builtin__.__import__
        __builtin__.__import__ = self._import
        self.newModules = {}
        
    def _import(self, name, globals=None, locals=None, fromlist=[]):
        result = apply(self.realImport, (name, globals, locals, fromlist))
        self.newModules[name] = 1
        return result
        
    def uninstall(self):
        for modname in self.newModules.keys():
            if not self.previousModules.has_key(modname) and modname in sys.modules and modname.startswith('pyerp'):
                # Force reload when modname next imported
                del(sys.modules[modname])
        __builtin__.__import__ = self.realImport

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
        r_imp = RollbackImporter()
        
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
        r_imp.uninstall()
        b_unittest.run_tests(self)

        connection.creation.destroy_test_db(old_name, 1)
        teardown_test_environment()


def find_pyerp_data():
    data_files = []
    root_dir = os.path.dirname(__file__)
    if root_dir != '':
        os.chdir(root_dir)
    src_dir = 'pyerp'
    for dirpath, dirnames, filenames in os.walk(src_dir):
        # Ignore dirnames that start with '.'
        for i, dirname in enumerate(dirnames):
            if dirname.startswith('.'): del dirnames[i]
        for f in filenames:
            if not f.endswith('.py') and not f.endswith('.pyc'):
                data_files.append(os.path.join(dirpath[len(src_dir)+1:], f))
    return data_files

r_imp = RollbackImporter()
version = __import__('pyerp').__version__
r_imp.uninstall()

setup(
    name = 'Pyerp', 
    version = version, 
    url = 'http://www.pyerp.cn/', 
    download_url = 'http://www.pyerp.cn/download/',
    author = 'Pyerp Software', 
    author_email = 'yuhere@gmail.com', 
    description = 'Integrated Financial CRM', 
    long_description = "Pyerp is a web-based software enterprise resource planning system. " \
                       "It provides an application framework and some plug-ins application." \
                       "ex. Financial application , CRM application, .",
    license = 'GPLv3', 
    classifiers = [ 
        'Environment :: Web Environment', 
        'Framework :: Pyerp ' + version, 
        'Intended Audience :: Developers', 
        'License :: OSI Approved ::GPLv3 License', 
        'Operating System :: OS Independent', 
        'Programming Language :: Python', 
        'Topic :: Software Development :: ERP System', 
        'Topic :: Software Development :: Financial CRM', 
    ], 
    packages = find_packages(exclude=['tests**']),
    package_data = {'pyerp' : find_pyerp_data()},
    test_suite = 'tests.suite',
    install_requires = [
        'setuptools>=0.6b1',
#        'Django>=1.0.2',
    ],
    entry_points = {
        'distutils.commands': [
            'pyerpunittest = setup:pyerpunittest'
        ],
    },
  )
