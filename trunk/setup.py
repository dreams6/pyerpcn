# -*- coding: utf-8 -*- 
from distutils.core import setup
from setuptools import setup, find_packages

version = __import__('pyerp').get_version()


setup(
    name = 'Pyerp', 
    version = version, 
    description = 'Integrated Financial CRM', 
    long_description = "Pyerp is a web-based software enterprise resource planning system. " \
                       "It provides an application framework and some plug-ins application." \
                       "ex. Financial application , CRM application, .",
    author = 'Pyerp Software', 
    author_email = 'yuhere@gmail.com', 
    license = 'GPLv3', 
    url = 'http://www.pyerp.cn/', 
    download_url = 'http://www.pyerp.cn/download/', 
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
    # package_dir={'pyerp': 'src/pyerp'},
    # packages=find_packages(exclude=['*.tests']),
    packages=find_packages(exclude=['tests**']),
    test_suite = 'tests.suite',
    #~ install_requires = [
        #~ 'Django>=1.0.2_final',
        #~ 'Genshi>=0.5'
    #~ ],
  )
