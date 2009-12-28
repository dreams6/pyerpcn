# -*- coding: utf-8 -*- 

from models import MessageResource

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
