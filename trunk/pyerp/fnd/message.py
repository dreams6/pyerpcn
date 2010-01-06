# -*- coding: utf-8 -*- 

from pyerp.fnd import models

from pyerp.fnd.utils.version import get_svn_revision, get_version

__svnid__ = '$Id$'
__svn__ = get_svn_revision(__name__)


#
# 
# 
#
def getmessagetext(name, lang="en"):
  msg = MessageResource.objects.get(name=name, language_code=lang)
  return msg.text

#
# 
# 
#
def getmessage(name, lang="en"):
  msg = MessageResource.objects.get(name=name, language_code=lang)
  return msg
