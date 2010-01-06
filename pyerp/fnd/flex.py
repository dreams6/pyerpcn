# -*- coding: utf-8 -*- 

import time

from django.conf import settings
from django.utils.cache import patch_vary_headers
from django.utils.http import cookie_date

from pyerp.fnd.utils.version import get_svn_revision, get_version

__svnid__ = '$Id$'
__svn__ = get_svn_revision(__name__)

