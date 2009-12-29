# -*- coding: utf-8 -*- 

from models import LookUpNode
from models import MessageResource
from pyerp.fnd.gbl import fnd_global



# LookUpNode===============================================================

#
# 
# 
#
def lookupmeaning(**arg):
  u"""\
    �?、指定されたIDで、node.meaningを取得する�??
    ②、指定された親IDと名前で、node.meaningを取得する�??
    ③、指定されたパスで、node.meaningを取得する�??
    ④、指定されたパスと名前で、node.meaningを取得する�??
    Arguments:
      id     - 
      path - 
      name   - \
  """
  if arg.has_key("id"):
    parent_node = LookUpNode.objects.get(pk=arg['id'])
    if arg.has_key("name"):
      node = LookUpNode.objects.get(parent_node=parent_node, name=arg['name'])
      return node.meaning
    else:
      return parent_node.meaning
  elif arg.has_key("path"):
    parent_node = LookUpNode.objects.get(node_path=arg['path'])
    if arg.has_key("name"):
      node = LookUpNode.objects.get(parent_node=parent_node, name=arg['name'])
      return node.meaning
    else:
      return parent_node.meaning
  return None

#
# 
# 
#
def lookuplist(**arg):
  u"""
  
  """
  if arg.has_key("id"):
    if arg['id'] is None:
      if arg.has_key("leaf"):
        return LookUpNode.objects.filter(parent_node__isnull=True, leaf_node=arg['leaf']).order_by('id')
      else:
        return LookUpNode.objects.filter(parent_node__isnull=True).order_by('id')
    else:
      parent_node = LookUpNode.objects.get(pk=arg['id'])
      if arg.has_key("leaf"):
        return LookUpNode.objects.filter(parent_node=parent_node, leaf_node=arg['leaf']).order_by('id')
      else:
        return LookUpNode.objects.filter(parent_node=parent_node).order_by('id')
  elif arg.has_key("path"):
    if arg['path'] is None:
      return None
    elif arg['path']=="/":
      if arg.has_key("leaf"):
        return LookUpNode.objects.filter(parent_node__isnull=True, leaf_node=arg['leaf']).order_by('id')
      else:
        return LookUpNode.objects.filter(parent_node__isnull=True).order_by('id')
    else:
      parent_node = LookUpNode.objects.get(node_path=arg['path'])
      if arg.has_key("leaf"):
        return LookUpNode.objects.filter(parent_node=parent_node, leaf_node=arg['leaf']).order_by('id')
      else:
        return LookUpNode.objects.filter(parent_node=parent_node).order_by('id')
  return None
  # return a list of parentnode or lookuppath

#
# 
# 
#
def addlookupnode(name, 
                  meaning, 
                  description=None, 
                  parentnodeid=None, 
                  leaf_node=False):

  node = LookUpNode()
  node.name = name
  node.meaning = meaning
  node.description = description
  node.leaf_node = leaf_node
  node.name = name
  if parentnodeid!=None:
    parent_node = LookUpNode.objects.get(pk=parentnodeid)
    node.parent_node = parent_node
    node.node_path = parent_node.node_path + "/" + name
  else:
    node.node_path = "/" + name

  node.enabled = True

  # ==============================
  node.created_by = fnd_global.user_id
  node.last_updated_by = fnd_global.user_id
  # ==============================
  node.save()
  return node

#
# 
# 
#
def init_lookup():
    node = addlookupnode("MSG_TYPE", "Message Type")
    addlookupnode("E", "Error", "Error.", node.id)
    addlookupnode("W", "Warning", "Warning.", node.id)
    addlookupnode("N", "Note", "Note.", node.id)
    addlookupnode("Q", "Question", "Question.", node.id)
    addlookupnode("H", "Hint", "Hint.", node.id)
    addlookupnode("T", "Tip", "Tip.", node.id)
    addlookupnode("P", "Prompt", "Prompt.", node.id)
    addlookupnode("M", "Menu", "Menu.", node.id)
    addlookupnode("O", "Other", "Other.", node.id)
    
    node = addlookupnode("MSG_CATEGORY", "Message Category")
    addlookupnode("SYS", "System", "System.", node.id)
    addlookupnode("USR", "User", "User.", node.id)
    addlookupnode("PRO", "Product", "Product.", node.id)
    addlookupnode("ERR", "Error", "Error.", node.id)
    addlookupnode("SEC", "Security", "Security.", node.id)
    addlookupnode("APP", "Application", "Application.", node.id)
    
    pass

# MessageText===============================================================

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

#
# 
# 
#
