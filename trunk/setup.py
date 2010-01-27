# -*- coding: utf-8 -*- 

from setuptools import setup, find_packages
import os
import sys

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



setup(
    name = 'Pyerp', 
    version = __import__('pyerp').__version__, 
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
        'Framework :: Pyerp ' + __import__('pyerp').__version__, 
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
            'pyerpunittest = tests.testrunner:pyerpunittest'
        ],
    },
  )
