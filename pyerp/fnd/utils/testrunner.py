# -*- coding: utf-8 -*-


from bitten.util.testrunner import unittest as b_unittest

class pyerpunittest(b_unittest):
    """
    add follow info into setup.py's setup() option
    entry_points = {
        'distutils.commands': [
            'pyerpunittest = pyerp.fnd.utils.testrunner:pyerpunittest'
        ],
    and run python setup.py egg_info first.(setuptools is required)
    
    """
    
    # TODO: define option Django's setting
    
    
    
    
    def run_tests(self):
        print "pyerpunittest.TODO. setup django unittest evn....."
        b_unittest.run_tests(self)
        print "pyerpunittest.TODO. distory django unittest evn....."
